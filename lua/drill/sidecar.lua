local M = {}

local _stdin = nil
local _handle = nil
local _pid = nil
local _linebuf = ""
local _effects = {}

local function _dispatch(line)
  -- luanil.object: decode JSON null to Lua nil (key absent) instead of vim.NIL.
  -- vim.NIL is userdata and *truthy*, which corrupts `or`-defaulting and any
  -- `if eff.field` test, and crashes on string concatenation in the winbar.
  local ok, eff = pcall(vim.json.decode, line, { luanil = { object = true } })
  if not ok or type(eff) ~= "table" then
    vim.schedule(function()
      vim.notify("[drill] bad effect JSON: " .. line, vim.log.levels.WARN)
    end)
    return
  end
  local name = eff.effect
  local cb = _effects[name]
  if cb then
    vim.schedule(function() cb(eff) end)
  end
end

local function _handle_data(err, data)
  if err then
    vim.schedule(function()
      vim.notify("[drill] sidecar error: " .. tostring(err), vim.log.levels.WARN)
    end)
    return
  end
  if not data then return end
  _linebuf = _linebuf .. data
  while true do
    local nl = _linebuf:find("\n")
    if not nl then break end
    local line = _linebuf:sub(1, nl - 1)
    _linebuf = _linebuf:sub(nl + 1)
    if line ~= "" then _dispatch(line) end
  end
end

function M.start(cfg)
  if M.is_running() then return end

  local python = cfg.python or { "uv", "run", "python" }
  local cmd = python[1]
  local args = {}
  for i = 2, #python do args[#args + 1] = python[i] end
  vim.list_extend(args, {
    "-m", "drill.client.nvim_host",
    "--url", cfg.url or "http://127.0.0.1:8000",
    "--user", cfg.user or "anon",
    "--timeout", tostring((cfg.run_timeout_ms or 5000) / 1000),
  })

  local stdin_pipe = vim.uv.new_pipe(false)
  local stdout_pipe = vim.uv.new_pipe(false)
  local stderr_pipe = vim.uv.new_pipe(false)

  local opts = {
    args = args,
    stdio = { stdin_pipe, stdout_pipe, stderr_pipe },
    cwd = cfg.cwd,
  }

  local handle, pid = vim.uv.spawn(cmd, opts, function(code, _signal)
    _handle = nil
    _pid = nil
    _stdin = nil
    vim.schedule(function()
      vim.notify("[drill] sidecar exited (code " .. code .. ")", vim.log.levels.INFO)
    end)
  end)

  if not handle then
    vim.notify("[drill] failed to spawn sidecar", vim.log.levels.ERROR)
    return
  end

  _handle = handle
  _pid = pid
  _stdin = stdin_pipe

  stdout_pipe:read_start(_handle_data)
  stderr_pipe:read_start(function(_err, data)
    if data then
      vim.schedule(function()
        vim.notify("[drill sidecar] " .. data, vim.log.levels.DEBUG)
      end)
    end
  end)
end

function M.send(cmd_tbl)
  if not _stdin then
    vim.notify("[drill] sidecar not running", vim.log.levels.WARN)
    return
  end
  _stdin:write(vim.json.encode(cmd_tbl) .. "\n")
end

function M.on_effect(name, cb)
  _effects[name] = cb
end

function M.off_effect(name)
  _effects[name] = nil
end

function M.is_running()
  return _handle ~= nil
end

function M.stop()
  if _stdin then _stdin:close() end
  if _handle then _handle:close() end
  _handle = nil
  _pid = nil
  _stdin = nil
  _linebuf = ""
end

return M
