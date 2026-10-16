local M = {}

local _cfg = nil
local _keymaps_installed = false

local function _sidecar() return require("drill.sidecar") end
local function _ui() return require("drill.ui") end

local function _wire_effects()
  local s = _sidecar()

  s.on_effect("set_buffer", function(e)
    _ui().set_answer_buffer(e.text or "")
    _ui().arm_first_keystroke(function()
      _sidecar().send({ cmd = "begin" })
    end)
  end)

  s.on_effect("question", function(e)
    _ui().clear_sections()
    local prompt = e.prompt or ""
    local lines = vim.split(prompt, "\n", { plain = true })
    _ui().set_section("PROMPT", "PROMPT", lines)
  end)

  s.on_effect("tests", function(e)
    _ui().clear_busy()
    local lines = {
      string.format("%d passed · %d failed", e.passed or 0, e.failed or 0),
    }
    for _, d in ipairs(e.detail or {}) do
      table.insert(lines, string.format("  ✗ %s: %s", d.name or "?", d.reason or ""))
    end
    if e.error then
      for _, l in ipairs(vim.split("error: " .. e.error, "\n", { plain = true })) do
        table.insert(lines, l)
      end
    end
    _ui().set_section("TESTS", "Tests", lines)
  end)

  s.on_effect("verdict", function(e)
    _ui().clear_busy()
    local lines = vim.split(e.text or "", "\n", { plain = true })
    _ui().set_section("VERDICT", "Verdict", lines)
  end)

  s.on_effect("hint", function(e)
    local lines = vim.split(e.text or "", "\n", { plain = true })
    _ui().set_section("HINT", "Hint", lines)
  end)

  s.on_effect("meta", function(e)
    _ui().update_meta(e)
  end)

  s.on_effect("status", function(e)
    -- Error/timeout path: the judge emits `status` instead of `verdict` on
    -- failure, so clear the busy token here to avoid it sticking.
    _ui().clear_busy()
    vim.notify("[drill] " .. (e.text or ""), vim.log.levels.INFO)
  end)

  s.on_effect("stats", function(e)
    vim.notify(e.text or "", vim.log.levels.INFO,
      { title = "drill stats: " .. (e.view or "") })
  end)
end

function M._open()
  local ui = _ui()
  ui.open(_cfg)
  if not _sidecar().is_running() then
    _sidecar().start(_cfg)
    _wire_effects()
  end
  if _cfg.keymaps and not _keymaps_installed then
    require("drill.keymaps").setup(_cfg)
    _keymaps_installed = true
  end
end

function M.cmd_next(keyword)
  M._open()
  _sidecar().send({ cmd = "next", keyword = keyword })
end

function M.cmd_test()
  _ui().set_busy("running tests")
  _sidecar().send({ cmd = "test", source = _ui().get_answer_source() })
end

function M.cmd_submit()
  _ui().set_busy("testing + submitting")
  _sidecar().send({ cmd = "submit", source = _ui().get_answer_source() })
end

function M.cmd_hint()
  _sidecar().send({ cmd = "hint" })
end

function M.cmd_cheat()
  _sidecar().send({ cmd = "cheat" })
end

function M.cmd_soon()
  _sidecar().send({ cmd = "soon" })
end

function M.cmd_bury()
  _sidecar().send({ cmd = "bury" })
end

function M.cmd_skip()
  _sidecar().send({ cmd = "skip" })
end

function M.cmd_restate()
  _sidecar().send({ cmd = "restate" })
end

function M.cmd_goto(identifier)
  M._open()
  _sidecar().send({ cmd = "goto", identifier = identifier })
end

function M.cmd_corpus(name)
  M._open()
  _sidecar().send({ cmd = "corpus", name = name })
end

-- Show a statistics view as a notification. view defaults to "session";
-- topic_keyword/date_range are optional filters parsed by the :Drill dispatcher.
function M.cmd_stats(view, topic_keyword, date_range)
  M._open()
  _sidecar().send({
    cmd = "stats",
    view = view or "session",
    topic_keyword = topic_keyword,
    date_range = date_range,
  })
end

-- Comment (flag) the current question. With no text, prompt for it; the
-- sidecar targets whatever question is currently loaded.
function M.cmd_comment(text)
  if text and text ~= "" then
    _sidecar().send({ cmd = "comment", text = text })
  else
    vim.ui.input({ prompt = "Drill comment: " }, function(input)
      if input and input ~= "" then
        _sidecar().send({ cmd = "comment", text = input })
      end
    end)
  end
end

-- Deactivate (retire) the current question, with an optional comment.
function M.cmd_deactivate(text)
  _sidecar().send({ cmd = "deactivate", text = text })
end

function M.setup(opts)
  _cfg = require("drill.config").merge(opts)

  vim.api.nvim_create_user_command("Drill", function(args)
    local parts = vim.split(args.args, "%s+")
    local sub = parts[1] or ""
    if sub == "" or sub == "next" then
      M.cmd_next(parts[2])
    elseif sub == "test" then
      M.cmd_test()
    elseif sub == "submit" then
      M.cmd_submit()
    elseif sub == "hint" then
      M.cmd_hint()
    elseif sub == "cheat" then
      M.cmd_cheat()
    elseif sub == "soon" then
      M.cmd_soon()
    elseif sub == "bury" then
      M.cmd_bury()
    elseif sub == "skip" then
      M.cmd_skip()
    elseif sub == "restate" then
      M.cmd_restate()
    elseif sub == "goto" then
      M.cmd_goto(parts[2])
    elseif sub == "corpus" then
      M.cmd_corpus(parts[2])
    elseif sub == "comment" then
      local text = vim.trim((args.args:gsub("^%s*comment%s*", "", 1)))
      M.cmd_comment(text ~= "" and text or nil)
    elseif sub == "deactivate" then
      local text = vim.trim((args.args:gsub("^%s*deactivate%s*", "", 1)))
      M.cmd_deactivate(text ~= "" and text or nil)
    elseif sub == "stats" then
      local view = parts[2]
      local topic_keyword, date_range
      for i = 3, #parts do
        local tok = parts[i]
        -- Date-range vocabulary mirrors the IPython magic; source of truth is
        -- DrillClient._date_filter / do_stats in drill/client/__init__.py.
        if tok == "today" or tok == "7days" or tok == "30days" or tok == "all" then
          date_range = tok
        elseif tok ~= "" then
          topic_keyword = tok
        end
      end
      M.cmd_stats(view, topic_keyword, date_range)
    else
      vim.notify("[drill] unknown subcommand: " .. sub, vim.log.levels.WARN)
    end
  end, { nargs = "*", desc = "Fluency Driller" })
end

return M
