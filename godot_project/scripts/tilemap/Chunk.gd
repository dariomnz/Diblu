extends TileMap

const CLEAR_WATER = 1
const DARK_WATER = 2
const GRASS = 5
const HIGH_GRASS = 3
const HIGH_WATER = 4
const SAND = 0

const decorations = {
	"GRASS":{
		"TREE":0,
		"GRASS":[2,3,4,5,6,7,8,9,10,11],
		"FLOWER":[15,16,17],
		"ROCK":[12,13,14]
	},
	"SAND":{
		"PALM_TREE":1,
		"STAR":[18,19],
		"SHELL":[20,21,22],
		"COCONUT":[23,24,25,28,29],
		"GRASS":[30,31,32],
		"ROCK":[33,34,35]
	}
}

const entities = {
	"CHICKEN":0,
	"DINO":1,
	"SKELETON":2,
}

var _childs = []

var noise1 : OpenSimplexNoise
var noise2 : OpenSimplexNoise

onready var decoration_tilemap : = $Decorations
onready var can_jump : = $"Can jump"
onready var entities_tilemap : = $Entities

var chunk_pos : Vector2

var should_remove = false

var rand : = RandomNumberGenerator.new()

var furniture_data_chunk = {}

func initialize(_chunk_pos,_noise1,_noise2,decoration_seed,_furniture_data_chunk):
	self.chunk_pos = _chunk_pos
	self.noise1 = _noise1
	self.noise2 = _noise2
	rand.seed = decoration_seed
	self.furniture_data_chunk = _furniture_data_chunk

	
func _ready():
	position = chunk_pos*(global_var.CHUNK_SIZE-Vector2(1,1))*global_var.TILE_SIZE
	create_chunk()
	
	create_furniture()

func create_chunk():
	# Creamos la capa principal del suelo
	for i in range(chunk_pos.x-2,chunk_pos.x+global_var.CHUNK_SIZE.x+3):
		for j in range(chunk_pos.y-2,chunk_pos.y+global_var.CHUNK_SIZE.y+3):
			var tile_type = tile_type_at_xy(i+(global_var.CHUNK_SIZE.x-1)*chunk_pos.x,j+(global_var.CHUNK_SIZE.y-1)*chunk_pos.y)
			set_cell(i,j,tile_type)
			update_bitmask_area(Vector2(i,j))
			
	# Arreglamos los picos
	var posible_no_type =[
			[[1,1,1],[1,0,1],[0,0,0]],
			[[0,0,0],[1,0,1],[1,1,1]],
			[[1,1,0],[1,0,0],[1,1,0]],
			[[0,1,1],[0,0,1],[0,1,1]]
			]
	for i in range(chunk_pos.x,chunk_pos.x+global_var.CHUNK_SIZE.x):
		for j in range(chunk_pos.y,chunk_pos.y+global_var.CHUNK_SIZE.y):
			var aux_data = same_cell_neirbours(i,j,get_cell(i,j))
			var count_no_type=aux_data[0]
			var arr_no_type=aux_data[1]
			var aux_tile_type = aux_data[2]
			if arr_no_type in posible_no_type or count_no_type>=6:
				set_cell(i,j,aux_tile_type)
				update_bitmask_area(Vector2(i,j))


	# Creamos las decoraciones y creacion del nuevo mapa para poder saltar tiles
	for i in range(chunk_pos.x-2,chunk_pos.x+global_var.CHUNK_SIZE.x+3):
		for j in range(chunk_pos.y-2,chunk_pos.y+global_var.CHUNK_SIZE.y+3):
			var cell_tipe = get_cell(i,j)
			if not (i < chunk_pos.x or i >= chunk_pos.x+global_var.CHUNK_SIZE.x or \
				j < chunk_pos.y or j >= chunk_pos.y+global_var.CHUNK_SIZE.y):	
				if same_cell_neirbours(i,j,cell_tipe)[0]==0:
					create_decorations(i,j,cell_tipe)
				
				create_entities(i,j,cell_tipe)

			if cell_tipe==HIGH_GRASS or cell_tipe==HIGH_WATER:
				can_jump.set_cell(i,j,0)
				can_jump.update_bitmask_area(Vector2(i,j))
				
	# Eliminamos los bordes exteriores que sobran sin actualizar autotile
	for i in range(chunk_pos.x-2,chunk_pos.x+global_var.CHUNK_SIZE.x+3):
		for j in range(chunk_pos.y-2,chunk_pos.y+global_var.CHUNK_SIZE.y+3):
			if i < chunk_pos.x or i >= chunk_pos.x+global_var.CHUNK_SIZE.x or \
				j < chunk_pos.y or j >= chunk_pos.y+global_var.CHUNK_SIZE.y:
					set_cell(i,j,-1)
					can_jump.set_cell(i,j,-1)
					
	# Añadimos las decoraciones
	decoration_tilemap.update_tile2obj()
	# Añadimos las entities
	entities_tilemap.update_tile2obj()
	
func same_cell_neirbours(x,y,tile_type):
	"""Devuelve una cuenta y un array de 0 con 1 en los vecinos diferentes"""
	var count_no_type = 0
	var arr_no_type = [[0,0,0],[0,0,0],[0,0,0]]
	
	var neirbour_type
	var di
	var dj

	for aux_i in range(-1,2):
		di=x+aux_i
		for aux_j in range(-1,2):
			dj=y+aux_j
			var get_cell_type = get_cell(di,dj)
			if get_cell_type != tile_type:
				neirbour_type = get_cell_type
				arr_no_type[aux_i+1][aux_j+1]=1
				count_no_type+=1

	return [count_no_type,arr_no_type,neirbour_type]
	
func tile_type_at_xy(x,y):
	var tile_type
	var noise_at_xy = noise_x_y(x,y)
	
	if noise_at_xy< -0.3:
			# Agua oscura
		tile_type=DARK_WATER
	elif noise_at_xy< -0.1:
			# Agua orilla
		tile_type=CLEAR_WATER
	elif noise_at_xy< 0.1:
			# Arena
		tile_type=SAND
	elif noise_at_xy< 0.3:
			# Cesped
		tile_type=GRASS
	elif noise_at_xy< 0.55:
	# Cesped elevado
		tile_type=HIGH_GRASS
	else:
		# Acua con cesped elevado
		tile_type=HIGH_WATER
	
	return tile_type
	
func noise_x_y(x,y):
	
	var noise_x_y1 = noise1.get_noise_2d(x,y)
	var noise_x_y2 = noise2.get_noise_2d(x,y)
	
	return (noise_x_y1*0.8+noise_x_y2*0.2)
	
func create_decorations(x,y,tile_type):
	var rand_num = rand.randi()%1000
	
	if tile_type == GRASS or tile_type == HIGH_GRASS:
		if rand_num < 30:
			if same_cell_neirbours(x+1,y+2,GRASS)[0]==0 or same_cell_neirbours(x+1,y+2,HIGH_GRASS)[0]==0:
				decoration_tilemap.set_cell(x,y,decorations["GRASS"]["TREE"])
		elif rand_num < 200:
			decoration_tilemap.set_cell(x,y,decorations["GRASS"]["GRASS"][rand.randi()%len(decorations["GRASS"]["GRASS"])])
		elif rand_num < 230:
			decoration_tilemap.set_cell(x,y,decorations["GRASS"]["FLOWER"][rand.randi()%len(decorations["GRASS"]["FLOWER"])])
		elif rand_num < 270:
			decoration_tilemap.set_cell(x,y,decorations["GRASS"]["ROCK"][rand.randi()%len(decorations["GRASS"]["ROCK"])])
			
	if tile_type == SAND:
		if rand_num < 40:
			if same_cell_neirbours(x+2,y+3,SAND)[0]==0:
				decoration_tilemap.set_cell(x,y,decorations["SAND"]["PALM_TREE"])
		elif rand_num < 70:
			decoration_tilemap.set_cell(x,y,decorations["SAND"]["STAR"][rand.randi()%len(decorations["SAND"]["STAR"])])
		elif rand_num < 100:
			decoration_tilemap.set_cell(x,y,decorations["SAND"]["SHELL"][rand.randi()%len(decorations["SAND"]["SHELL"])])
		elif rand_num < 130:
			decoration_tilemap.set_cell(x,y,decorations["SAND"]["COCONUT"][rand.randi()%len(decorations["SAND"]["COCONUT"])])
		elif rand_num < 160:
			decoration_tilemap.set_cell(x,y,decorations["SAND"]["GRASS"][rand.randi()%len(decorations["SAND"]["GRASS"])])
		elif rand_num < 190:
			decoration_tilemap.set_cell(x,y,decorations["SAND"]["ROCK"][rand.randi()%len(decorations["SAND"]["ROCK"])])
		
func create_entities(x,y,tile_type):
	
	var rand_num = rand.randi()%1000
	
	if tile_type == GRASS or tile_type == HIGH_GRASS:
		if rand_num < 2:
			entities_tilemap.set_cell(x,y,entities["CHICKEN"])
		elif rand_num < 4:
			entities_tilemap.set_cell(x,y,entities["DINO"])
		elif rand_num < 9:
			entities_tilemap.set_cell(x,y,entities["SKELETON"])

func create_furniture():
	for _filename in furniture_data_chunk.keys():
		for id in furniture_data_chunk[_filename].keys():
			
			var furniture = load(_filename).instance()
			
			furniture.id = id
			
			_childs.append(furniture)
			furniture.connect("destroy",self,"delete_child")
			get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",furniture)
	
	
func spawn_item(position,item_name,amount=1):
	var item = preload("res://prefabs/entity/item/Item.tscn").instance()
	
	item.initialize(position,item_name,amount)
	
	_childs.append(item)
	item.connect("pickup",self,"delete_child")
	get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",item)
	
func is_water(check_position):
	check_position -= position
	check_position = world_to_map(check_position)
	
	return get_cellv(check_position) == CLEAR_WATER

func delete_child(child):
#	print(furniture_data_chunk)
	if child.filename in furniture_data_chunk:
		if child.id in furniture_data_chunk[child.filename]:
#		print(furniture_data_chunk)
#			print(furniture_data_chunk[child.filename][child.id])
			furniture_data_chunk[child.filename].erase(child.id)
			
#			print(furniture_data_chunk[child.filename][child.id])
			var key = str(chunk_pos.x)+","+str(chunk_pos.y)
			get_parent().furniture_data[key][child.filename].erase(child.id)
			
			if len(furniture_data_chunk[child.filename]) == 0:
				furniture_data_chunk.erase(child.filename)
				get_parent().furniture_data[key].erase(child.filename)
				
			if len(furniture_data_chunk) == 0:
				get_parent().furniture_data.erase(key)
	
	if child in _childs:
		_childs.erase(child)
	
func queue_free():
	for child in get_children():
		child.queue_free()
	for child in _childs:
		child.queue_free()
	.queue_free()
