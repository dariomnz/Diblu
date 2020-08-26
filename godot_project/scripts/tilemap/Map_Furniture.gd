extends TileMap

const Crate = preload("res://prefabs/tilemap/tiles/Crate.tscn")
const CrateID = 0

const Campfire = preload("res://prefabs/tilemap/tiles/Campfire.tscn")
const CampfireID = 1

var actual_item_image
func _ready():
	set_process(false)

func _process(_delta):
	var position_map = world_to_map(get_global_mouse_position())
	clear()
	
	var slot = get_tree().get_nodes_in_group("inventory")[0].slot_focus
	if slot.get_child_count() != 0:
		actual_item_image = slot.get_children()[0]
		if actual_item_image:
			if actual_item_image.item_name in global_var.POSIBLE_FURNITURE:
				set_cellv(position_map,global_var.POSIBLE_FURNITURE[actual_item_image.item_name])
				$Timer.start()

func replaceCrates():
	var tileArr = get_used_cells_by_id(CrateID)
	for tile in tileArr:
		var newCrate = Crate.instance()
		var tilepos = map_to_world(tile)
		var adjustment = Vector2(32/2,32/2)
		newCrate.set_position(tilepos + adjustment)
		set_cell(tile.x,tile.y,-1)
		
		add_to_chunk(newCrate)
		
		
		
func replaceCampfire():
	var tileArr = get_used_cells_by_id(CampfireID)
	for tile in tileArr:
		var newCampfire = Campfire.instance()
		var tilepos = map_to_world(tile)
		var adjustment = Vector2(32/2,32/2+10)
		newCampfire.set_position(tilepos + adjustment)
		set_cell(tile.x,tile.y,-1)
		
		add_to_chunk(newCampfire)
		
		
func add_to_chunk(obj):
	var chunk = get_parent().get_chunk_by_position(obj.position)
	
	chunk._childs.append(obj)
	obj.connect("destroy",chunk,"delete_child")
	get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",obj)
	
	var chunk_key = str(chunk.chunk_pos.x)+","+str(chunk.chunk_pos.y)
	save(chunk_key, obj)
	
func construct_mode():
	set_process(true)
	

func contruct():
	get_tree().get_nodes_in_group("inventory")[0].remove_amount(actual_item_image,1)
			
	replaceCrates()
	replaceCampfire()


func _on_Timer_timeout():
	set_process(false)
	clear()

func save(chunk_key,obj):
	var data = get_parent().furniture_data
	
	if not chunk_key in data:
		data[chunk_key] = {}
		
	data = data[chunk_key]
		
	if not obj.filename in data:
		data[obj.filename]={}
	
	data = data[obj.filename]
	
	if not obj.id in data:
		data[obj.id] = 0
		
