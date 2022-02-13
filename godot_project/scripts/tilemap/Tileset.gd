tool
extends TileSet

const CLEAR_WATER = 1
const DARK_WATER = 2
const GRASS = 5
const HIGH_GRASS = 3
const HIGH_WATER = 4
const SAND = 0

# Solo se marca el tipo que tiene que no crear borde
var binds = {
	CLEAR_WATER:[DARK_WATER],
	DARK_WATER:[],
	GRASS:[SAND],
	HIGH_GRASS:[HIGH_WATER],
	HIGH_WATER:[],
	SAND:[CLEAR_WATER]
}

func _is_tile_bound(drawn_id, neighbor_id):
	if drawn_id in binds:
		return neighbor_id in binds[drawn_id]
	return false
