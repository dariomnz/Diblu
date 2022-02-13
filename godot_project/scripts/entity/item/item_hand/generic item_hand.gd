extends Position2D

class_name Item_hand

onready var item_sprite : = $Item

onready var player : = get_parent()

onready var actionPlayer :AnimationPlayer = $ActionPlayer

var item_name

var current_rotation_degrees : int setget set_current_rotation_degrees

func _ready():
	
	var new_item_image = null
	
	if item_name:
		var item_image_path = "res://assets/entity/item/"+item_name+".png"
		new_item_image = load(item_image_path)
	
	item_sprite.texture = new_item_image

func _process(_delta):
	
	var direction = global_position.direction_to(get_global_mouse_position())
	var degrees = rad2deg( direction.angle())
	
	set_current_rotation_degrees(degrees)
	
func _unhandled_input(_event):

	if Input.is_action_just_pressed("ui_left_click"):
		action(1)
	if Input.is_action_just_pressed("ui_right_click"):
		action(2)
	
	if item_name and item_name in global_var.POSIBLE_FURNITURE:
			get_tree().get_nodes_in_group("Chunk_control")[0].construct_mode()
	
func action(number: int):
	var animation_name = "action"+str(number)
	if actionPlayer.has_animation(animation_name) and not actionPlayer.is_playing():
		actionPlayer.play(animation_name)
		
	if has_method(animation_name):
		call(animation_name)
		
func construct():
	if item_name and item_name in global_var.POSIBLE_FURNITURE:
		get_tree().get_nodes_in_group("Chunk_control")[0].construct()

func set_current_rotation_degrees(newRotation_degrees):
	if newRotation_degrees > 90 or newRotation_degrees < -90:
		scale = Vector2(-1,1)
		rotation_degrees = newRotation_degrees -180
	else:
		scale = Vector2(1,1)
		rotation_degrees = newRotation_degrees
	current_rotation_degrees = newRotation_degrees
