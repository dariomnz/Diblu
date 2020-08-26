extends TileMap


var camera : KinematicBody2D
var world : YSort

var furniture_data = {}

var active_chunks = {}
var unready_chunks = {}
var thread : Thread

var noise2=OpenSimplexNoise.new()

var noise1=OpenSimplexNoise.new()

var decoration_seed = randi()

func _ready():
	cell_size=global_var.CHUNK_SIZE*global_var.TILE_SIZE
	
	camera = get_tree().get_nodes_in_group("player")[0]
	world = get_tree().get_nodes_in_group("world")[0]
	
	noise1.seed=randi()
	noise1.octaves=8
	noise1.period=40
	noise1.persistence=0.1
	noise1.lacunarity=0.4
	
	noise2.seed=randi()
	noise2.octaves=8
	noise2.period=10
	noise2.persistence=0.1
	noise2.lacunarity=0.5
	
	thread = Thread.new()
	
	load_furniture()

func _exit_tree():
	save_furniture()

func add_chunk(chunk_pos):
	var key = str(chunk_pos.x)+","+str(chunk_pos.y)
	if active_chunks.has(key) or unready_chunks.has(key):
		return
		
	if not thread.is_active():
		var _err = thread.start(self,"load_chunk", [thread,chunk_pos])
		unready_chunks[key] = 1
		
func load_chunk(arr):
	var _thread = arr[0]
	var chunk_pos = arr[1]
	
	var chunk = preload("res://prefabs/tilemap/Chunk.tscn").instance()
	var key = str(chunk_pos.x)+","+str(chunk_pos.y)
	var furniture_data_chunk = {}
	if key in furniture_data:
		furniture_data_chunk = furniture_data[key]
	chunk.initialize(chunk_pos,noise1,noise2,decoration_seed,furniture_data_chunk)
	
	call_deferred("load_done",chunk,_thread)

func load_done(chunk,_thread):
	add_child(chunk)
	var key = str(chunk.chunk_pos.x)+","+str(chunk.chunk_pos.y)
	active_chunks[key] = chunk
	unready_chunks.erase(key)
	set_cellv(chunk.chunk_pos,0)
	_thread.wait_to_finish()
	
func remove_chunk(chunk):
	if not thread.is_active():
		var _err = thread.start(self,"_remove_chunk", [thread,chunk])
	
func _remove_chunk(arr):
	var _thread = arr[0]
	var chunk = arr[1]
	
	call_deferred("remove_done",chunk,_thread)
	
func remove_done(chunk,_thread):
	var key = str(chunk.chunk_pos.x)+","+str(chunk.chunk_pos.y)
	active_chunks.erase(key)
	chunk.queue_free()
	_thread.wait_to_finish()
	
func get_chunk(chunk_pos):
	var key = str(chunk_pos.x)+","+str(chunk_pos.y)
	if active_chunks.has(key):
		return active_chunks[key]
	return null

func _process(_delta):
	update_chunks()
	clean_up_chunks()
	reset_chunks()
	
func update_chunks():
	var check_pos = world_to_map(camera.position)
	
	var chunk_amount = global_var.CHUNK_AMOUNT
	var zoom = get_tree().get_nodes_in_group("camera")[0].current_zoom
	if zoom < Vector2(3,3):
		chunk_amount*=zoom
	else:
		chunk_amount*=Vector2(3,3)
	
	for x in range(check_pos.x - chunk_amount.x * 0.5-1, check_pos.x + chunk_amount.x * 0.5+2):
		for y in range(check_pos.y - chunk_amount.y * 0.5-1, check_pos.y + chunk_amount.y * 0.5+2):
			var chunk_pos = Vector2(x,y)
			add_chunk(chunk_pos)
			var chunk = get_chunk(chunk_pos)
			if chunk != null:
				chunk.should_remove = false
	
func clean_up_chunks():
	for key in active_chunks:
		var chunk = active_chunks[key]
		if chunk.should_remove:
			remove_chunk(chunk)
				
func reset_chunks():
	for key in active_chunks:
		active_chunks[key].should_remove = true
		
		
func spawn_item(position,item_name,amount=1):
	var chunk = get_chunk_by_position(position)
	
	if chunk:
		chunk.spawn_item(position,item_name,amount)
		
		
func get_chunk_by_position(gorld_position):
	var chunk_pos = world_to_map(gorld_position)
	
	var key = str(chunk_pos.x)+","+str(chunk_pos.y)
	
	if key in active_chunks:
		return active_chunks[key]
		
	return null

var furniture_directory_path = "res://save/chunk/"
var furniture_file_name = "furniture.save"

func save_furniture():
	var file : = File.new()
	var directory : = Directory.new()
	
	var _err = directory.make_dir_recursive(furniture_directory_path)
	
	_err = file.open(furniture_directory_path+furniture_file_name,File.WRITE)
	
	file.store_line(to_json(furniture_data))
	
	file.close()
	
func load_furniture():
	
	var file : = File.new()
	
	if file.file_exists(furniture_directory_path + furniture_file_name):
		var _err = file.open(furniture_directory_path + furniture_file_name,File.READ)
		
		var text = file.get_as_text()
		
		furniture_data = parse_json(text)
		
	file.close()

func construct_mode():
	$Furniture.construct_mode()
	
	
func construct():
	$Furniture.contruct()
