def environment_action(action):
  if action == "arrival":
      return {
          "environment": "arrival_mode",
          "lights": "soft_on",
          "music": "welcome_track",
          "screen": "welcome_message"
      }
  elif action == "activity":
      return {
          "environment": "activity_mode",
          "lights": "bright",
          "music": "upbeat",
          "screen": "game_prompt"
      }
  elif action == "energy":
      return {
          "environment": "energy_boost",
          "lights": "pulse",
          "music": "high_energy",
          "screen": "challenge_prompt"
      }
  elif action == "moment":
      return {
          "environment": "moment_event",
          "lights": "flash",
          "music": "arena_hit",
          "screen": "moment_display"
      }
  elif action == "standby":
      return {
          "environment": "standby_mode",
          "lights": "dim",
          "music": "ambient",
          "screen": "idle_message"
      }
  else:
      return {
          "environment": "no_action"
      }
