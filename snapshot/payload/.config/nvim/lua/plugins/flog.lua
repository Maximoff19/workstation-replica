return {
  {
    "rbong/vim-flog",
    cmd = { "Flog", "Flogsplit", "Floggit" },
    dependencies = {
      "tpope/vim-fugitive",
    },
    keys = {
      {
        "<leader>gl",
        "<cmd>Flogsplit<cr>",
        desc = "Open git log graph",
      },
    },
  },
}
