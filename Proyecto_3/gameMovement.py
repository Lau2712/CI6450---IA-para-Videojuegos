import math

def handle_pathfinding_movement_exp2(player_x, player_y, current_path, tile_size, world_width, world_height, pathfinding_speed):
    if not current_path:
        return player_x, player_y
        
    # Get next node in path
    next_node = current_path[0].to_node
    target_x = next_node.x * tile_size
    target_y = next_node.y * tile_size
    
    # Calculate direction to target
    dx = target_x - player_x
    dy = target_y - player_y
    distance = math.sqrt(dx * dx + dy * dy)
    
    # If we reached current node, move to next node
    if distance < tile_size/2:
        current_path.pop(0)
        if not current_path:
            return player_x, player_y
        next_node = current_path[0].to_node
        target_x = next_node.x * tile_size
        target_y = next_node.y * tile_size
        dx = target_x - player_x
        dy = target_y - player_y
        distance = math.sqrt(dx * dx + dy * dy)
    
    if distance > 0:
        # Normalize direction and apply speed
        dx = (dx / distance) * pathfinding_speed
        dy = (dy / distance) * pathfinding_speed
        
        # Calculate new position
        new_x = player_x + dx
        new_y = player_y + dy
        
        # Mantener dentro de los límites del mundo
        new_x = max(0, min(world_width, new_x))
        new_y = max(0, min(world_height, new_y))
        
        return new_x, new_y
        
    return player_x, player_y

def handle_pathfinding_movement(player_x, player_y, current_path, tile_size, world_width, world_height, pathfinding_speed, scaled_maze):
    if not current_path:
        return player_x, player_y
        
    # Get next node in path
    next_node = current_path[0].to_node
    target_x = next_node.x * tile_size 
    target_y = next_node.y * tile_size

    # Calculate direction to target
    dx = target_x - player_x
    dy = target_y - player_y
    distance = math.sqrt(dx * dx + dy * dy)
    
    # If stuck, try alternative movements
    if distance < pathfinding_speed:
        # Try moving diagonally
        if not check_collision(player_x + pathfinding_speed, player_y + pathfinding_speed, scaled_maze):
            return player_x + pathfinding_speed, player_y + pathfinding_speed
        # Try moving horizontally
        elif not check_collision(player_x + pathfinding_speed, player_y, scaled_maze):
            return player_x + pathfinding_speed, player_y
        # Try moving vertically  
        elif not check_collision(player_x, player_y + pathfinding_speed, scaled_maze):
            return player_x, player_y + pathfinding_speed
    
    if distance > 0:
        # Normalize direction and apply speed
        dx = (dx / distance) * pathfinding_speed
        dy = (dy / distance) * pathfinding_speed
        
        # Calculate new position
        new_x = player_x + dx
        new_y = player_y + dy
        
        # Check collision before moving
        if not check_collision(new_x, new_y, scaled_maze):
            return new_x, new_y
            
    return player_x, player_y

def check_collision(x, y, scaled_maze):
    try:
        color = scaled_maze.get_at((int(x), int(y)))
        return color[0] < 246 
    except IndexError:
        return True

def handle_pathfinding_movement_player(current_x, current_y, path, tile_size, world_width, world_height, speed, maze=None):
    # Get next waypoint from path
    next_waypoint = path[0].to_node
    target_x = next_waypoint.x * tile_size + tile_size/2 
    target_y = next_waypoint.y * tile_size + tile_size/2

    # Calculate direction to target
    dx = target_x - current_x
    dy = target_y - current_y
    distance = math.sqrt(dx*dx + dy*dy)

    # If very close to waypoint, move to next one
    if distance < tile_size/4:
        path.pop(0)
        if len(path) > 0:
            next_waypoint = path[0].to_node
            target_x = next_waypoint.x * tile_size + tile_size/2
            target_y = next_waypoint.y * tile_size + tile_size/2
            dx = target_x - current_x 
            dy = target_y - current_y
            distance = math.sqrt(dx*dx + dy*dy)

    if distance > 0:
        # Normalize direction
        dx = dx/distance
        dy = dy/distance

        # Calculate new position
        new_x = current_x + dx * speed
        new_y = current_y + dy * speed

        # Check diagonal movement
        if abs(dx) > 0.5 and abs(dy) > 0.5:
            # Try moving horizontally first
            temp_x = current_x + dx * speed
            if not check_collision(temp_x, current_y, maze):
                new_x = temp_x
                current_x = new_x
            
            # Then try moving vertically
            temp_y = current_y + dy * speed
            if not check_collision(current_x, temp_y, maze):
                new_y = temp_y

        # Keep within world bounds
        new_x = max(0, min(world_width, new_x))
        new_y = max(0, min(world_height, new_y))

        return new_x, new_y

    return current_x, current_y