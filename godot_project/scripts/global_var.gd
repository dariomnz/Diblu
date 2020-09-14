extends Node

const CHUNK_SIZE = Vector2(16,16)
const TILE_SIZE = Vector2(16,16)

const CHUNK_AMOUNT = Vector2(3,2)

const ITEM_STACK_LIMIT = 256

const POSIBLE_FURNITURE = {
	"crate":0,
	"campfire":1,
}

const NORMAL_KNOCKBACK = 200

enum {UP,DOWN,LEFT,RIGHT}

enum {HORIZONTAL=1,VERTICAL=2}

var is_debug = true
