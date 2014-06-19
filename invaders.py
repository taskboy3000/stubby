import pygame,GameThings

game = { "screen_dimensions" : (500,500),
         # "display_flags" : pygame.FULLSCREEN,
         "show_mouse" : False,
         "bgcolor" : (16,16,16),
         "bgcolor_victory" : (255,128,128),
         "title" : "Stubby Invaders",
         "background_song" : "music/014.mod",
         "font" : "Ethnocen.ttf",
         "debug" : 0
       }

game["map"] = [
               [ 1, 0, 1, 1, 1, 0, 1, 1, 0, 1], 
               [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [ 0, 1, 0, 0, 0, 1, 0, 0, 1, 0],
               [ 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
              ]

game["tiles"] = [ "",
                  "gfx/brick.bmp",
                  "gfx/gold_sm.bmp",
                ]

game["sounds"] = { 
                   "got_gold" : "sound/dong.wav",
                   "victory"  : "sound/yaahooo.wav"
                 }

dude = GameThings.MovableThing({"filenames" : [ "gfx/dude1.bmp",
                                                "gfx/dude2.bmp",
                                                "gfx/dude3.bmp",
                                                "gfx/dude4.bmp",
                                                ], 
                                "default_speed" : 5, 
                                "start_cell_position" : (5,9),
				"vertical_move_only" : 0,
			        "horizontal_move_only" : 1,
                                }) 

booze1 = GameThings.MovableThing({ "filenames" : ["gfx/booze0.bmp",
                                                  "gfx/booze1.bmp",
                                                 ], 
                                   "default_speed" : 2, 
                                   "start_cell_position" : (1,1),
                                   "animation_speed" : 10,
                                   "ai_movement" : "invader_march",
                                   "name" : "Boozey1",
				   "last_move" : "left",
				   "points" : 25
                                 }
                                 )

booze2 = GameThings.MovableThing({ "filenames" : ["gfx/booze0.bmp",
                                                  "gfx/booze1.bmp",
                                                 ], 
                                   "default_speed" : 2, 
                                   "start_cell_position" : (2,1),
                                   "animation_speed" : 10,
                                   "ai_movement" : "invader_march",
                                   "name" : "Boozey2",
				   "last_move" : "right",
				"points" : 25,

                                 }
                                 )

game["movables"] = [dude];

G = GameThings.GameEngine(game)

G.play();
