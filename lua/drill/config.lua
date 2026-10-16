local M = {}

M.defaults = {
  url = "http://127.0.0.1:8000",
  user = "anon",
  python = { "uv", "run", "python" },
  cwd = nil,
  fluency_mode = true,
  run_timeout_ms = 5000,
  layout = "vertical",
  info_width = 60,        -- prompt/info pane width  (vertical layout)
  info_height = 15,       -- prompt/info pane height (horizontal layout)
  info_wrap = true,       -- word-wrap (wrap + linebreak) the prompt/info pane
  info_filetype = "text",  -- filetype of the prompt/info pane (markdown conceals code markup)
  keymaps = true,
}

function M.merge(opts)
  return vim.tbl_deep_extend("force", M.defaults, opts or {})
end

return M
