try:
    from files.HUD import iniciar_hud
except ModuleNotFoundError as erro:
    if erro.name != "files":
        raise
    from HUD import iniciar_hud


if __name__ == "__main__":
    iniciar_hud()
