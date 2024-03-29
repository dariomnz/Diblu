extends TileMap

const Chicken = preload("res://prefabs/entity/Chicken/Chicken.tscn")
const ChickenID = 0

const Dino = preload("res://prefabs/entity/Dino/Dino.tscn")
const DinoID = 1

const Skeleton = preload("res://prefabs/entity/Skeleton/Skeleton.tscn")
const SkeletonID = 2

#var _childs = []

func _ready():
	update_tile2obj()
	

func update_tile2obj():
	var chickens = get_used_cells_by_id(ChickenID)
	var dinos = get_used_cells_by_id(DinoID)
	var skeletons = get_used_cells_by_id(SkeletonID)
	
	replaceChickens(chickens)
	replaceDinos(dinos)
	replaceSkeletons(skeletons)

func replaceChickens(tileArr):
	var tilepos
	for tile in tileArr:
		var newChicken = Chicken.instance()
		tilepos = map_to_world(tile)#+get_parent().position
		newChicken.set_position(tilepos)
		set_cell(tile.x,tile.y,-1)
#		_childs.append(newChicken)
#		newChicken.connect("death",self,"delete_child")
#		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",newChicken)
		get_parent().call_deferred("add_child",newChicken)

func replaceDinos(tileArr):
	var tilepos
	for tile in tileArr:
		var newDino = Dino.instance()
		tilepos = map_to_world(tile)#+get_parent().position
		newDino.set_position(tilepos)
		set_cell(tile.x,tile.y,-1)
#		_childs.append(newDino)
#		newDino.connect("death",self,"delete_child")
#		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",newDino)
		get_parent().call_deferred("add_child",newDino)

func replaceSkeletons(tileArr):
	var tilepos
	for tile in tileArr:
		var newSkeleton = self.Skeleton.instance()
		tilepos = map_to_world(tile)#+get_parent().position
		newSkeleton.set_position(tilepos)
		set_cell(tile.x,tile.y,-1)
#		_childs.append(newSkeleton)
#		newSkeleton.connect("death",self,"delete_child")
#		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",newSkeleton)
		get_parent().call_deferred("add_child",newSkeleton)

#func delete_child(child):
#	if child in _childs:
#		_childs.erase(child)

#func queue_free():
#	for child in _childs:
#		child.queue_free()
#	.queue_free()
