import pygame,GameThings

game = { "screen_dimensions" : (500,500),
         # "display_flags" : pygame.FULLSCREEN,
         "show_mouse" : False,
         "bgcolor" : (255,255,128),
         "bgcolor_victory" : (255,128,128),
         "title" : "Stubby Falls Down",
         "background_song" : "music/bg.mp3",
         "font" : "Ethnocen.ttf",
         "debug" : 0
       }

game["maps"] = [
                # level 1
                [
                 [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                 [ 1, 0, 0, 1, 1, 1, 0, 1, 2, 1],
                 [ 1, 0, 0, 1, 1, 0, 0, 1, 0, 1],
                 [ 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
                 [ 1, 1, 1, 0, 1, 0, 0, 1, 0, 1],
                 [ 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
                 [ 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                 [ 1, 0, 1, 0, 0, 0, 1, 1, 1, 1],
                 [ 1, 2, 1, 0, 1, 2, 1, 1, 1, 1],
                 [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                ],
                # level 2
                [
                 [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                 [ 1, 2, 1, 0, 2, 0, 1, 1, 2, 1],
                 [ 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                 [ 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                 [ 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                 [ 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                 [ 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                 [ 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
                 [ 1, 0, 0, 0, 1, 0, 1, 1, 1, 1],
                 [ 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
                ],
               ]

game["tiles"] = [ "",
                  "gfx/brick.bmp",
                  "gfx/gold_sm.bmp",
                ]

game["sounds"] = { 
                   "got_gold" : "sound/coin_4.wav",
                   "weapon"   : "sound/axe_throw.wav",
                   "drinking" : "sound/burp_1.wav",
                   "victory"  : "sound/yaahooo.wav",
                   "failed"   : "sound/glass_crash.wav",
                 }

dude = GameThings.MovableThing({"filenames" : ["gfx/dude1.bmp",
                                                "gfx/dude2.bmp",
                                                "gfx/dude3.bmp",
                                                "gfx/dude4.bmp",
                                                ], 
                                "default_speed" : 5, 
                                "start_cell_position" : (5,5),
				"last_move" : "left",
                                }) 

game["movables"] = [dude];

G = GameThings.GameEngine(game)

G.play();
