local M = {}

local _cfg = nil
local _tab = nil
local _ans_buf = nil
local _ans_win = nil
local _info_buf = nil
local _info_win = nil
local _sections = {}
local _meta = { topic = "", question_id = nil, hints_total = 0, hints_shown = 0, due_count = 0, new_count = 0 }
local _timer = nil
local _elapsed = 0
local _busy = nil          -- transient winbar label, e.g. "submitting"
local _busy_timeout = nil  -- libuv one-shot safety net
local _ks_group = vim.api.nvim_create_augroup("DrillFirstKeystroke", { clear = true })

local function _render_winbar()
  if not _ans_win or not vim.api.nvim_win_is_valid(_ans_win) then return end
  local topic = _meta.topic or ""
  local qid = _meta.question_id
  local id_str = qid and ("Q" .. qid) or "—"
  local mm = math.floor(_elapsed / 60)
  local ss = _elapsed % 60
  local timer_str = string.format("⏱ %02d:%02d", mm, ss)
  local pips = ""
  for i = 1, _meta.hints_total do
    pips = pips .. (i <= _meta.hints_shown and "●" or "○")
  end
  local busy = _busy and string.format(" ⧗ %s… ", _busy) or ""
  -- Available-question counts from the last fetch (due/new), shown only while a
  -- question is active. Replaces the chatty "N available" status notification.
  local queue = qid and string.format(" · %dd/%dn", _meta.due_count or 0, _meta.new_count or 0) or ""
  local bar = string.format(" %s · %s · %s%s  hints %s %s", topic, id_str, timer_str, queue, pips, busy)
  vim.api.nvim_set_option_value("winbar", bar, { win = _ans_win })
end

local function _render_info()
  if not _info_buf or not vim.api.nvim_buf_is_valid(_info_buf) then return end
  local lines = {}
  for _, sec in ipairs(_sections) do
    table.insert(lines, "── " .. sec.header .. " ──")
    for _, l in ipairs(sec.lines) do
      -- nvim_buf_set_lines rejects any item containing a newline, so flatten
      -- embedded newlines (e.g. multi-line vim.inspect output or tracebacks)
      -- into separate buffer lines.
      for _, sub in ipairs(vim.split(l, "\n", { plain = true })) do
        table.insert(lines, sub)
      end
    end
    table.insert(lines, "")
  end
  vim.api.nvim_set_option_value("modifiable", true, { buf = _info_buf })
  vim.api.nvim_buf_set_lines(_info_buf, 0, -1, false, lines)
  vim.api.nvim_set_option_value("modifiable", false, { buf = _info_buf })
end

local function _start_timer()
  if _timer then return end
  _elapsed = 0
  _timer = vim.uv.new_timer()
  _timer:start(1000, 1000, vim.schedule_wrap(function()
    _elapsed = _elapsed + 1
    _render_winbar()
  end))
end

local function _stop_timer()
  if _timer then
    _timer:stop()
    _timer:close()
    _timer = nil
  end
  _elapsed = 0
end

local function _make_ans_buf()
  local buf = vim.api.nvim_create_buf(false, false)
  vim.api.nvim_set_option_value("filetype", "python", { buf = buf })
  vim.api.nvim_set_option_value("omnifunc", "", { buf = buf })
  if _cfg and _cfg.fluency_mode then
    vim.api.nvim_buf_set_var(buf, "cmp_enabled", false)
    vim.api.nvim_buf_set_var(buf, "copilot_enabled", false)
  end
  return buf
end

local function _make_info_buf()
  local buf = vim.api.nvim_create_buf(false, true)
  vim.api.nvim_set_option_value("buftype", "nofile", { buf = buf })
  vim.api.nvim_set_option_value("modifiable", false, { buf = buf })
  local ft = (_cfg and _cfg.info_filetype) or "markdown"
  vim.api.nvim_set_option_value("filetype", ft, { buf = buf })
  return buf
end

local function _tab_is_valid()
  if not _tab then return false end
  for _, t in ipairs(vim.api.nvim_list_tabpages()) do
    if t == _tab then return true end
  end
  return false
end

function M.open(cfg)
  _cfg = cfg
  if _tab_is_valid() then
    vim.api.nvim_set_current_tabpage(_tab)
    return
  end
  vim.cmd("tabnew")
  _tab = vim.api.nvim_get_current_tabpage()

  _ans_buf = _make_ans_buf()
  vim.api.nvim_win_set_buf(0, _ans_buf)
  _ans_win = vim.api.nvim_get_current_win()

  _info_buf = _make_info_buf()
  if (cfg.layout or "vertical") == "vertical" then
    -- belowright: force the new (info) window to the RIGHT regardless of the
    -- user's 'splitright'; a plain :vsplit honors it and could put the prompt
    -- on the left.
    vim.cmd("belowright vsplit")
    vim.api.nvim_win_set_width(0, cfg.info_width or 60)
  else
    -- aboveleft: force the new (info) window on TOP regardless of the user's
    -- 'splitbelow'; a plain :split honors it and drops the prompt below the
    -- editor.
    vim.cmd("aboveleft split")
    vim.api.nvim_win_set_height(0, cfg.info_height or 15)
  end
  vim.api.nvim_win_set_buf(0, _info_buf)
  _info_win = vim.api.nvim_get_current_win()
  -- Never conceal in the info panel: it shows code-bearing prompts/hints
  -- (kv[0], *args, backticks). LazyVim sets conceallevel=2 globally and
  -- render-markdown would hide that markup; force conceal off on this window
  -- regardless of filetype.
  vim.api.nvim_set_option_value("conceallevel", 0, { win = _info_win })
  vim.api.nvim_set_option_value("concealcursor", "", { win = _info_win })
  -- Word-wrap the prompt pane. `wrap` alone breaks mid-word; `linebreak`
  -- makes it break at spaces. Set explicitly on this window so it holds
  -- regardless of the user's global 'wrap'/'nowrap' default.
  if cfg.info_wrap ~= false then
    vim.api.nvim_set_option_value("wrap", true, { win = _info_win })
    vim.api.nvim_set_option_value("linebreak", true, { win = _info_win })
  end

  vim.api.nvim_set_current_win(_ans_win)
  _render_winbar()
end

function M.set_answer_buffer(text)
  if not _ans_buf or not vim.api.nvim_buf_is_valid(_ans_buf) then return end
  local lines = vim.split(text, "\n", { plain = true })
  vim.api.nvim_buf_set_lines(_ans_buf, 0, -1, false, lines)
  if _ans_win and vim.api.nvim_win_is_valid(_ans_win) then
    vim.api.nvim_win_set_cursor(_ans_win, { #lines, 0 })
  end
end

function M.get_answer_source()
  if not _ans_buf or not vim.api.nvim_buf_is_valid(_ans_buf) then return "" end
  return table.concat(vim.api.nvim_buf_get_lines(_ans_buf, 0, -1, false), "\n")
end

-- Arm a one-shot autocmd: the next time the user enters insert mode in the
-- answer buffer, call on_first() exactly once. Clearing the group first drops
-- any still-pending arm from a prior question (the answer buffer is reused),
-- so a fresh question never inherits a stale trigger. InsertEnter does not fire
-- on the programmatic stub write, so the populate never trips it.
function M.arm_first_keystroke(on_first)
  if not _ans_buf or not vim.api.nvim_buf_is_valid(_ans_buf) then return end
  vim.api.nvim_clear_autocmds({ group = _ks_group, buffer = _ans_buf })
  vim.api.nvim_create_autocmd("InsertEnter", {
    group = _ks_group,
    buffer = _ans_buf,
    once = true,
    callback = function() on_first() end,
  })
end

function M.set_section(key, header, lines)
  for _, sec in ipairs(_sections) do
    if sec.key == key then
      sec.header = header
      sec.lines = lines
      _render_info()
      return
    end
  end
  table.insert(_sections, { key = key, header = header, lines = lines })
  _render_info()
end

function M.clear_sections()
  _sections = {}
  _render_info()
end

local function _clean(v)
  -- Guard against JSON null surviving as vim.NIL (truthy userdata) regardless
  -- of how the effect was decoded; map both nil and vim.NIL to plain nil.
  if v == nil or v == vim.NIL then return nil end
  return v
end

function M.update_meta(eff)
  local qid = _clean(eff.question_id)
  _meta = {
    topic = _clean(eff.topic) or "",
    question_id = qid,
    hints_total = _clean(eff.hints_total) or 0,
    hints_shown = _clean(eff.hints_shown) or 0,
    due_count = _clean(eff.due_count) or 0,
    new_count = _clean(eff.new_count) or 0,
  }
  if qid then
    _start_timer()
  else
    _stop_timer()
  end
  _render_winbar()
end

-- Show a transient busy label in the winbar (e.g. "submitting"). Renders
-- synchronously so the bar changes in the same frame as the keypress rather
-- than on the next 1s timer tick. Arms a generous one-shot timer as a backstop
-- against a dead sidecar that never replies; this is not the normal clear path,
-- so it must stay well above the LLM judge timeout (default 30s).
function M.set_busy(label)
  _busy = label
  if _busy_timeout then
    _busy_timeout:stop()
    _busy_timeout:close()
  end
  _busy_timeout = vim.uv.new_timer()
  _busy_timeout:start(60000, 0, vim.schedule_wrap(function() M.clear_busy() end))
  _render_winbar()
end

function M.clear_busy()
  _busy = nil
  if _busy_timeout then
    _busy_timeout:stop()
    _busy_timeout:close()
    _busy_timeout = nil
  end
  _render_winbar()
end

return M
