-- stylua: ignore
-- selene: allow(undefined_variable)
---@diagnostic disable-next-line: undefined-global
USER.load_local_config({
    use_session        = true, -- Use local session
    use_spellfile      = false, -- Use local spell file
    use_palettes       = false, -- Use local palettes
    use_prettier       = true, -- Copy .prettierrc from templates folder
    use_editorconfig   = true, -- Copy .editorconfig from templates folder
    use_format_on_save = true, -- Enable LSP format on save
})
