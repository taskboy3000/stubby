import sys,os.path,pygame,random
"""

These classes help to make a generic arcade game

"""
import copy

class MovableThing :

        #---------------------------------------------------
        def __init__ (self, args):
                # attempt to load all like image names
                self.filenames = args["filenames"]
                
                # to be filled in later
                self.img    = []
                self.current_image = 0
                self.height = -1
                self.width  = -1
                self.pos    = (-1,-1)
		self.points = 0
		self.gold = 0

		if args.has_key("points") :
			self.points = args["points"]

                if args.has_key("pos") :
                        self.pos = args["pos"]

		self.vertical_move_only = 0
		if args.has_key("vertical_move_only") :
			self.vertical_move_only = args["vertical_move_only"]

		self.horizontal_move_only = 0
		if args.has_key("horizontal_move_only") :
			self.horizontal_move_only = args["horizontal_move_only"]

                self.start_position = (-1,-1)
                if args.has_key("start_cell_position") :
                        self.start_position = ((args["start_cell_position"][0]*50),
                                                (args["start_cell_position"][1]*50))
                
                self.name = "The Dude"
                if args.has_key("name") :
                    self.name = args["name"]
 
                self.created = 0
                self.collisions = {} # thing => tick_of_last_collision

                # contains global game info
                self.game = ""

                self.speed = args["default_speed"]
                self.default_speed = args["default_speed"]

                self.drunkness = 0
                self.last_swig = 0
                self.last_move = "up"

                if args.has_key("last_move") :
                   self.last_move = args["last_move"]

                self.tick = 0
                
                self.stopped = 0
                if args.has_key("ai_movement") :
                   self.ai_tracking = args["ai_movement"]
                else :
                   self.ai_tracking = "none"

                self.animation_speed = 0
                self.last_move_tick = 0
                if args.has_key("animation_speed") :
                   self.animation_speed = args["animation_speed"]
                else :
                   self.animation_speed = 5

        #---------------------------------------------------
        def initGraphics (self, game) :
                i=0
                while (i < len(self.filenames)) :                
                   self.img.append(pygame.image.load(self.filenames[i]).convert())
                   self.img[i].set_colorkey((255,255,255))
                   i += 1

                self.height = self.img[self.current_image].get_height()  
                self.width  = self.img[self.current_image].get_width()
                self.game   = game
                self.created = pygame.time.get_ticks()

                if self.start_position != (-1,-1) :
                   self.pos = self.get_current_surface().get_rect().move(self.start_position[0],self.start_position[1])
                else :
                   self.pos = self.get_current_surface().get_rect().move(self.pos[0],self.pos[1])
        
        #---------------------------------------------------
        def isDude (self) :
           return self.name.find("Dude") >= 0

        #---------------------------------------------------
        def isBoozey (self) : 
           return self.name.find("Boozey") >= 0

        #---------------------------------------------------
        def isFire(self) :
           return self.name.find("fire") >= 0

        #---------------------------------------------------
        def get_current_surface (self) :
            return self.img[self.current_image]

        #---------------------------------------------------
        def do_maintenance (self) :
            # a generic method to handle per-tick updates
	    1                
        #---------------------------------------------------
        def update_animation (self) :
             self.tick += 1
             if (self.tick > self.animation_speed) :
                # update current image
                if (self.current_image + 1 >= len(self.img)) :
                    self.current_image = 0
                else :
                    self.current_image += 1
                self.tick = 0

        #---------------------------------------------------
        def update_ai_movement(self) :
            # is this AI controlled?
            if self.ai_tracking == "none" :
                return 0

            if self.game.debug > 4 :
                print "AI move: %s\n" % self.ai_tracking

            # What king of move to make?
            directions = ["up","down","right","left",""]
            direction = ""
            if self.ai_tracking == "random" :
                # Should I change directions?
                if (self.last_move_tick + 1500) < pygame.time.get_ticks() :

                   direction = directions[random.randint(0,(len(directions)-1))]
                   if self.game.debug > 4 :
                      print "Moving AI %s\n" % direction
                   if direction != "" :
                      self.move(direction)
                   else :
                      if self.game.debug > 4 :
                        print "Not moving %s this turn\n" % self.name
                else :
                   if self.game.debug > 4 :
                        print "Not enough game ticks have passed for an AI move\n"
                   self.move(self.last_move)

            elif self.ai_tracking == "straight" :
                if self.game.debug > 4 :
                    print "Moving %s straight '%s'\n" % (self.name, self.last_move)

                if self.move(self.last_move) < 1 :
                    if self.game.debug > 4 :
                        print "Cannot move %s, so destroying\n" % self.name
                    self.game.remove_movable(self)

 	    elif self.ai_tracking == "invader_march" : 
		if self.game.debug > 4 : 
		    print "Marching %s '%s'\n" % (self.name, self.last_move)
	
		last_move = self.last_move
		if self.move(self.last_move) < 1 :
		   dir = "left"
		   if last_move == "left" :
			dir = "right"

		   if self.game.debug > 4 :
			print "Changing direction from %s to %s\n" % (last_move,dir)

		   self.last_move = dir
		   self.pos = (self.pos[0],self.pos[1]+50)
		   self.move(self.last_move)
				                 
        #---------------------------------------------------
        def handle_collision (self,source) :
            # This MT has been hit by source MT

            now = pygame.time.get_ticks()
            if self.collisions.has_key(source.name) :
                if (self.collisions[source.name] + 750 > now) :
                        if self.game.debug > 6 :
                            print "  A collision with %s occurred too recently\n" % source.name
                        return 0

            if source.collisions.has_key(self.name) :
                if (source.collisions[self.name] + 750 > now) :
                        if self.game.debug > 6 :
                            print "  A collision with %s occurred too recently\n" % source.name
                        return 0

            if self.game.debug > 3 :
                print "  %s has touched %s\n" % (self.name,source.name)
  
            self.collisions[source.name] = now
            source.collisions[self.name] = now

            # Next, figure out what to do when thing hits self
            
            # handle fire
        
            if (self.isFire() and source.isBoozey()) or (self.isBoozey() and source.isFire()) :
                if self.game.debug > 3 : 
                        print "  Removing Boozey and fire\n"

                self.game.remove_movable(self)
                self.game.remove_movable(source)

                # make a noise
                self.game.sfx["weapon"].set_volume(0.25)         
                self.game.sfx["weapon"].play()
	
		# add points to score
		self.game.score += self.points

            # Handle boozey catching dude
	    if (self.isDude() and source.isBoozey()) or (self.isBoozey() and source.isDude()) :
		if self.game.debug > 3 :
		    print "  Dude got caught by the Booze\n"

		# Make noise
                self.game.sfx["drinking"].set_volume(0.25)         
                self.game.sfx["drinking"].play()
		
                dude = self
                if source.isDude() : 
                   dude = source
        
		# remove points
		dude.game.score -= 25
                
                # increment drunkness
                dude.drunkness += 1
                dude.speed -= 1
                dude.last_swig = now

                if dude.speed <= 0 :
                   dude.game.do_dude_dies()

		# remove booze
		if source.isBoozey() :
	 		self.game.remove_movable(source)
		else :
			self.game.remove_movable(self)

        #---------------------------------------------------
        def move (self,direction="up") :
                pos = (0,0)

                if self.stopped == 1 :
                        return 0
		# is this move allowed?
		if self.horizontal_move_only and (direction == "up" or direction == "down") :
		   if self.game.debug > 5 :
		      print "[POLICY] Cannot move '%s'\n" % direction
		   self.last_move = direction
		   return 1

		if self.vertical_move_only and (direction == "left" or direction == "right") :
		   if self.game.debug > 5 :
		      print "[POLICY] Cannot move '%s'\n" % direction
		   self.last_move = direction
		   return 1

		# figure out new position
                if direction == "up" :
                   pos = (self.pos[0], (self.pos[1] - self.speed))
                elif direction == "down" :
                   pos = (self.pos[0], (self.pos[1] + self.speed))
                elif direction == "left" :
                   pos = ((self.pos[0] - self.speed), self.pos[1])
                elif direction == "right" :
                   pos = ((self.pos[0] + self.speed), self.pos[1])
                else :
                   if self.game.debug > 5 :
                      print "Cannot move '%s' in direction '%s'\n" % (self.name,direction)
                   return 0
                
                # calculate 4 points of the rect
                # none can enter a forbidden cell

                # wall dimensions are the key
                wall_width  = self.game.tiles[1].get_width()
                wall_height = self.game.tiles[1].get_height()
                dude_width  = self.width
                dude_height = self.height

                # fudge factor - XXX only makes sense for certain orientations
                x_border = -1
                y_border = -1

                nw_cell = ((pos[0]) / wall_width), ((pos[1])/ wall_height)
                ne_cell = ((pos[0] + dude_width + x_border) / wall_height), nw_cell[1]
                sw_cell = nw_cell[0], (pos[1] + dude_width + y_border) / wall_height 
                se_cell = ne_cell[0], (pos[1] + dude_height + y_border) / wall_height

		# are cell values in line with map?
		quads = [nw_cell,ne_cell,sw_cell,se_cell]
		for i,v in enumerate(quads) :

		  if v[0] >= len(self.game.map)  :
		 	quads[i] = (len(self.game.map) - 1,v[1])
		  if v[0] < 0 : 
			quads[i] = (0,v[1])

		  if v[1] >= len(self.game.map[0])  :
		 	quads[i] = (v[0],len(self.game.map[0]) - 1)
		  if v[1] < 0 : 
			quads[i] = (v[0],0)
		
                if self.game.debug > 9:
                   print "Can %s move to cell (%d,%d) from (%d,%d)?\n" \
                         % (self.name,pos[0],pos[1],self.pos[0], self.pos[1])

		   print "  NW (%d,%d) NE (%d,%d) SW (%d,%d) SE (%d,%d)\n" \
                        % (quads[0][0],quads[0][1],\
                           quads[1][0],quads[1][1],\
                           quads[2][0],quads[2][1],\
                           quads[3][0],quads[3][1],)

                   print "  Map objects: NW [%d] NE [%d] SW [%d] SE [%d]\n" \
                        % (self.game.map[quads[0][1]][quads[0][0]],\
                           self.game.map[quads[1][1]][quads[1][0]],\
                           self.game.map[quads[2][1]][quads[2][0]],\
                           self.game.map[quads[3][1]][quads[3][0]],)


                rc = 0
                # will any of these fall off the map?
		screen_size = self.game.screen_dimensions
		if pos[0] >= screen_size[0] \
		   or pos[0] < 0 \
	 	   or pos[1] >= screen_size[1] \
		   or pos[1] < 0 :
			rc = 0
		else :
			rc = 1

                # will any of these corners hit a wall?
                if rc == 1 and self.game.map[quads[0][1]][quads[0][0]] != 1 \
                   and self.game.map[quads[1][1]][quads[1][0]] != 1 \
                   and self.game.map[quads[2][1]][quads[2][0]] != 1 \
                   and self.game.map[quads[3][1]][quads[3][0]] != 1 :
                   # Nope!  Move it!

                   self.pos = self.img[self.current_image].get_rect().move(pos[0],pos[1])
                   self.last_move = direction
                   self.last_move_tick = pygame.time.get_ticks()
                   
                   rc = 1

                else :
                   # print "  no\n"
                   self.last_move = ""

                return rc

#----------------------------------------------------------------
#----------------------------------------------------------------

class GameEngine :
    #---------------------------------------------------
    def __init__ (self,args) :
        self.screen = 0;
        self.screen_dimensions = args["screen_dimensions"];

        if args.has_key("display_flags") :
                self.display_flags = args["display_flags"]
        else :
                self.display_flags = 0
        
        self.title = args["title"]

        self.map = [[]]
        if args.has_key("map") :
               self.map = args["map"]

        self.maps = [[[]]]
        self.current_map = 0
        if args.has_key("maps") :
                self.maps = args["maps"]
                self.map = copy.deepcopy(self.maps[0])

        self.debug = args["debug"]
        self.score = 0

        # Set up tiles
        self.tile_files = args["tiles"];
        self.tiles = []
        self.game_over = 0
        self.level = 1
        self.dudes_left = 2

        self.bgcolor = args["bgcolor"]
        self.bgcolor_victory = args["bgcolor_victory"]

        # get sprites
        self.movables = args["movables"]

        if args.has_key("show_mouse") :
                self.show_mouse = args["show_mouse"]
        else :
                self.show_mouse = False

        # set up sounds
        self.sfx_files = args["sounds"]
        self.sfx = {}

        self.background_song = args["background_song"]

        # set up font
        self.font_filename = args["font"]

    #---------------------------------------------------
    def initGameObjects(self) :
        pygame.init()
        
        self.screen = pygame.display.set_mode(self.screen_dimensions, self.display_flags)
        pygame.display.set_caption(self.title)

        if self.show_mouse == 0 :
                pygame.mouse.set_visible(self.show_mouse)

        for t in self.tile_files :
           s = 0
           if os.path.exists(t) :
                if self.debug > 4 :
                        print "Loading tile file: %s\n" % t        
                s = pygame.image.load(t).convert()
                s.set_colorkey((255,255,255))
           self.tiles.append(s)
            
        for s in self.movables :
             s.initGraphics(self)

        # key => filename
        for s in self.sfx_files.keys() : 
            if os.path.exists(self.sfx_files[s]) :
                self.sfx[s] = pygame.mixer.Sound(self.sfx_files[s]);
            else :
                print "Could not find [%s] %s\n" % s, self.sfx_files[s];

        # set up background song
        if os.path.exists(self.background_song) :
                pygame.mixer.music.load(self.background_song)
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)

        self.font = pygame.font.Font(self.font_filename,20);
        self.font_victory = pygame.font.Font(self.font_filename, 32)
    #---------------------------------------------------
    def get_dude(self) :
        return self.movables[0]

    #---------------------------------------------------
    def fire_weapon(self) :
        if self.debug > 3 :
           print "Attempting to fire weapon\n"

        # first, look through movables for "fire"
        shots_left = 3
        last_shot = self.get_dude()
        now = pygame.time.get_ticks()
        for m in self.movables :
                if m.name.find("fire") >= 0 :
                        shots_left -= 1
                        if m.created < last_shot.created :
                                last_shot = m
                               

        if shots_left < 1 :
            if self.debug > 3 :
                print "Cannot fire additional shots\n"
            return 0
        
        # also, weapon cannot fire more than 1 every .5 second
        # find the last shot
        if (last_shot.created + 500) > now :
            if self.debug > 3 :
                print "Too soon to fire again (now: %d, last shot: %d)\n" % (now, (last_shot.created + 500))
            return 0

        # OK to fire
        if self.debug > 3 :
           print "Creating new Fire MovableThing\n"

        dude = self.get_dude()
        last_move = "right"
        if dude.last_move != "" :
            last_move = dude.last_move

        f = MovableThing({ "name" : "fire" + str(pygame.time.get_ticks()),
                           "filenames" : ["gfx/shot0.bmp",
                                          "gfx/shot1.bmp",
                                       ],
                          "default_speed"   : 8,
                          "pos"             : dude.pos,
                          "ai_movement"     : "straight",
                          "last_move"       : last_move,
                          "animation_speed" : 5
                          })

        f.initGraphics(self)
        self.movables.append(f)
        
    #---------------------------------------------------
    def handle_events(self) :
        # process events
        moved = 0
        dude = self.movables[0];

        for e in pygame.event.get():
                if e.type == pygame.QUIT:
                        sys.exit()

                if e.type == pygame.KEYDOWN :

                        if e.key == pygame.K_ESCAPE :
                                sys.exit()

                        if self.game_over == 0 :
                                if e.key == pygame.K_UP    : 
                                        if dude.move("up") : moved = 1
                                if e.key == pygame.K_DOWN  : 
                                        if dude.move("down") : moved = 1
                                if e.key == pygame.K_LEFT  : 
                                        if dude.move("left") : moved = 1
                                if e.key == pygame.K_RIGHT : 
                                        if dude.move("right") : moved = 1
                                if e.key == pygame.K_SPACE :
                                        # fire, if possible
                                        self.fire_weapon()

        # end of event check
        if moved < 1 and dude.last_move :
                dude.move(dude.last_move)

    #---------------------------------------------------
    def remove_movable(self, victim) :
        tmp = []

	if self.debug > 9 :
	    print "%d movable objects\n" % len(self.movables)

        for m in self.movables : 
           if m.name != victim.name :
              tmp.append(m)
	   else :
	      if self.debug > 9 :
		 print "Removed %s\n" % m.name

	if self.debug > 9 :
	    print "%d movable objects left\n" % len(tmp)

        self.movables = tmp

    #---------------------------------------------------
    def handle_collisions (self) :
	if self.game_over > 0 :
		return 0

        # What cell is Dude in? Should I divde by dude's size or tile size?  
        # I think tile
        dude = self.movables[0]
        cell = (dude.pos[0] / 50), (dude.pos[1] / 50)

	# should handle this generically.  The gold should be an MT    
        if self.map[cell[1]][cell[0]] == 2 :
                if self.debug > 10 :
                        print "Got gold!\n"

                # make a noise
                self.sfx["got_gold"].set_volume(0.25)         
                self.sfx["got_gold"].play()

                # change the map
                self.map[cell[1]][cell[0]] = 0

                # increment score
                self.score += 25           
		dude.gold += 1

		# Make dude less drunk
		if dude.drunkness > 0 :
		   dude.drunkness -= 1
		   dude.speed += 1 

	# did the player win?
        if dude.gold == 3 : 
            self.do_next_screen()

	cnt_boozeys = 0
        for m in self.movables : 
           for o in self.movables :
                if m.name == o.name :
                    continue;

                if m.name.find("Boozey") >= 0 :
		    cnt_boozeys += 1

		if not isinstance(m.pos, pygame.Rect) :
                    if self.debug > 0 :
		        print "%s.pos isn't a Rect;  Can't detect collision\n" % m.name
	            continue;

		if self.debug > 6 :
		   print "Has %s collided with %s?\n" % (m.name, o.name)
		   print "  (%d,%d) with (%d,%d)\n" % \
			(m.pos[0],m.pos[1],o.pos[0],o.pos[1])

		if isinstance(o.pos, pygame.Rect) :
                   if m.pos.colliderect(o.pos) :
                     m.handle_collision(o)
                else :
                   if self.debug > 0 :
		      print "%s's pos isn't a Rect\n" % o.name

	while (cnt_boozeys < 5) :
	    # create new boozey
            if self.debug > 5 :
		print "Creating new Boozey\n"

	    b = MovableThing({ "filenames" : ["gfx/booze0.bmp","gfx/booze1.bmp"],
			       "default_speed" : 2,
			       "animation_speed" : 10,
			       "ai_movement" : "random",
			       "name" : "Boozey" + str(pygame.time.get_ticks()),
			       "last_move" : "left",
			       "points" : 25,
			       "start_cell_position" : self.get_random_open_map_cell_position(),
		             })

	    self.movables.append(b)
	    b.initGraphics(self)

	    cnt_boozeys += 1
	    
    #---------------------------------------------------
    def handle_screen (self) :
        # paint bg
        if self.game_over :
           self.screen.fill(self.bgcolor_victory)
        else :
           self.screen.fill(self.bgcolor)

        # paint tiles
        # what the hell is the python idiom for this?
        x = 0
        y = 0
        while x < len(self.map) :
          while y < len(self.map[0]) :
            it = self.map[x][y]

            if self.debug > 10 :
                   print ("map %d,%d : tile %d\n" % (x,y,it))

            if it > 0 :
                # make a new wall or money bag
                if it >= len(self.tiles) :
                   print "  ** Don't seem to have a gfx for tile type %d\n" % it
                else : 
                  tile_tmp = self.tiles[it].copy()
                  self.screen.blit(tile_tmp, (y*50,x*50)) # shouldn't this use tile dims?

            y += 1

          y = 0
          x += 1

        # paint grid
        if self.debug > 5 :
           x = 50; # seems like this should come from the tile definition?
           while x < 500 :
             pygame.draw.line(self.screen,(0,0,255),(x,0),(x,500))
             x += 50

           y = 50;
           while y < 500 :
             pygame.draw.line(self.screen,(0,0,255),(0,y),(500,y))
             y += 50
 
        # paint dudes
        for i in self.movables :
            i.update_animation()
            i.do_maintenance()
            i.update_ai_movement()
            self.screen.blit(i.img[i.current_image], i.pos)

        # paint score
        text = self.font.render("Score: %04d" % self.score, 1, (255,255,255),(0,0,0,0))
        tr = text.get_rect()
        self.screen.blit(text, tr)


        # paint level
        text = self.font.render("Level: %01d" % self.level, 1, (255,255,255),(0,0,0,0))
        tr = text.get_rect(bottomleft=(0,500))
        self.screen.blit(text, tr)

        # Paint Dude's remaining
        dude = self.get_dude()
        lives = self.screen.subsurface(pygame.Rect((425,475),(75,25)))
        lives.fill((0,0,0,0))

        for i in range(0,self.dudes_left) :
          tr = dude.img[0].get_rect(bottomleft=((i*25),25))
          lives.blit(dude.img[0],tr)

        # paint drunkness
        text = self.font.render("Drunk: %01d" % dude.drunkness, 1, (255,255,255),(0,0,0,0))
        tr = text.get_rect(topright=(500,0))
        self.screen.blit(text, tr)

        if self.game_over > 0 :
           text = self.font_victory.render("Game over!", 1, (255,255,255),(0,0,0))
           tr = text.get_rect()
           tr.centerx = self.screen.get_rect().centerx
           tr.centery = self.screen.get_rect().centery

           self.screen.blit(text, tr)

        pygame.display.flip()
    #---------------------------------------------------
    def get_random_open_map_cell_position (self) :

        pos = (-1,-1)

        while 1 :
            x = random.randint(1,len(self.map)-1)
            y = random.randint(1,len(self.map[0])-1)

            # should not put this on the dude...
            if self.map[y][x] == 0 : 
                pos = (x,y)
                break

        return pos
    #---------------------------------------------------
    def do_next_screen (self) :
        # next screen
        next_map = self.current_map + 1
        if next_map > (len(self.maps) - 1) :
           next_map = 0

        # need a deep array copy        
        self.map = copy.deepcopy(self.maps[next_map])
        self.current_map = next_map
        self.level += 1

        # reset dude's gold counter
        dude = self.get_dude()
        dude.gold = 0
        new_pos = self.get_random_open_map_cell_position()
        dude.pos = (new_pos[0]*50,new_pos[1]*50)
        dude.last_move = ""

        # remove all boozeys and fire
        for m in self.movables :
            if m.name.find("Boozey") >= 0 :
               self.remove_movable(m)
            if m.name.find("fire") >= 0 :
               self.remove_movable(m)

        # pause?
        self.splashScreen("Ready?")

    #---------------------------------------------------
    def do_game_over(self,succeeded=0) :     
        self.game_over = 1

        # Stop background music
        pygame.mixer.music.stop()

        # stop movables
        for i in self.movables :
            i.stopped = 1
            i.move(i.last_move)
            self.screen.blit(i.img[i.current_image], i.pos)
        
        # play victory noise
        if succeeded > 0 :
          self.sfx["victory"].set_volume(0.5)
          self.sfx["victory"].play()
        else : 
          self.sfx["failed"].set_volume(0.25)
          self.sfx["failed"].play()

        # "gray out" screen
        self.handle_screen()

    #---------------------------------------------------
    def splashScreen (self,msg="") :
        if msg == "" :
          msg = self.title

        text = self.font_victory.render(msg, 1, (255,255,255),(0,0,0))
        tr = text.get_rect()
        tr.centerx = self.screen.get_rect().centerx
        tr.centery = self.screen.get_rect().centery

        self.screen.blit(text, tr)
        pygame.display.flip()
        pygame.time.wait(2500)

    #---------------------------------------------------
    def do_dude_dies (self) : 
        self.dudes_left -= 1
        if self.dudes_left >= 0 :
            dude = self.get_dude()
            new_pos = self.get_random_open_map_cell_position()
            dude.pos = (new_pos[0]*50,new_pos[1]*50)
            dude.drunkness = 0
	    dude.speed = dude.default_speed
            self.splashScreen("Try again!")
        else :
          self.do_game_over(0)
        
    #---------------------------------------------------
    def play(self) :
        self.initGameObjects()
        self.splashScreen()

        while 1 :
                self.handle_events()
                self.handle_collisions()
                self.handle_screen()
                pygame.time.delay(25)

