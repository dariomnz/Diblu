extends TileMap

const Tree = preload("res://prefabs/tilemap/tiles/Tree.tscn")
const TreeID = 0

const Palm_tree = preload("res://prefabs/tilemap/tiles/Palm tree.tscn")
const Palm_treeID = 1
# Declare member variables here. Examples:
# var a = 2
## var b = "text"
#var trees = []
#var palm_trees = []

#var _childs = []

func _ready():
	update_tile2obj()

func update_tile2obj():
	var Trees = get_used_cells_by_id(TreeID)
	var Palm_trees = get_used_cells_by_id(Palm_treeID)
	
	replaceTree(Trees)
	replacePalm_tree(Palm_trees)

func replaceTree(tileArr):
	var tilepos
	for tile in tileArr:
		var newTree = Tree.instance()
		tilepos = map_to_world(tile)#+get_parent().position
		newTree.set_position(tilepos)
		set_cell(tile.x,tile.y,-1)
#		_childs.append(newTree)
		get_parent().call_deferred("add_child",newTree)
#		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",newTree)
		
func replacePalm_tree(tileArr):
	var tilepos
	for tile in tileArr:
		var newTree = Palm_tree.instance()
		tilepos = map_to_world(tile)#+get_parent().position
		newTree.set_position(tilepos)
		set_cell(tile.x,tile.y,-1)
#		_childs.append(newTree)
		get_parent().call_deferred("add_child",newTree)
#		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",newTree)

#func queue_free():
#	for child in _childs:
#		child.queue_free()
#	.queue_free()
	

