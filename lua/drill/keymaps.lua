local M = {}

function M.setup(cfg)
  if not cfg.keymaps then return end
  -- which-key (and other keymap-help UIs) build their labels from each map's
  -- `desc`. Without it the leader popup shows a blank, textless entry.
  local function map(lhs, rhs, desc)
    vim.keymap.set("n", lhs, rhs, { buffer = true, silent = true, desc = desc })
  end
  local d = require("drill.init")
  map("<leader>dn", d.cmd_next, "Drill: next question")
  map("<leader>dt", d.cmd_submit, "Drill: test + submit (gated)")
  map("<leader>dT", d.cmd_test, "Drill: run tests")
  map("<leader>dh", d.cmd_hint, "Drill: next hint")
  map("<leader>dc", d.cmd_cheat, "Drill: reveal canonical answer")
  map("<leader>da", d.cmd_soon, "Drill: repeat this soon")
  map("<leader>db", d.cmd_bury, "Drill: bury (I've got this)")
  map("<leader>dr", d.cmd_restate, "Drill: restate prompt + stub")
  map("<leader>dk", d.cmd_skip, "Drill: skip question")
  map("<leader>dm", d.cmd_comment, "Drill: comment/flag current question")
  map("<leader>dx", d.cmd_deactivate, "Drill: deactivate current question")
  map("<leader>dS", function() require("drill.init").cmd_stats("session") end, "Drill: session stats")

  -- Label the <leader>d group (otherwise it inherits LazyVim's DAP "debug"
  -- group name in the popup). Buffer-local so it only applies in the drill tab.
  -- Guarded + version-tolerant: which-key v3 uses add(), v2 used register().
  local ok, wk = pcall(require, "which-key")
  if ok then
    if wk.add then
      wk.add({ { "<leader>d", group = "drill", buffer = 0 } })
    elseif wk.register then
      wk.register({ ["<leader>d"] = { name = "drill" } }, { buffer = 0 })
    end
  end
end

return M
