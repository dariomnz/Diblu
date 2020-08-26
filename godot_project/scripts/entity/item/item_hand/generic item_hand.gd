extends Position2D

class_name Item_hand

onready var item_sprite : = $Item

onready var player : = get_parent()

onready var actionPlayer :AnimationPlayer = $ActionPlayer

var item_name

func _ready():
	
	var new_item_image = null
	
	if item_name:
		var item_image_path = "res://assets/entity/item/"+item_name+".png"
		new_item_image = load(item_image_path)
	
	item_sprite.texture = new_item_image

func _process(_delta):
	
	var direction = global_position.direction_to(get_global_mouse_position())
	var degrees = rad2deg( direction.angle())
	
	if degrees > 90 or degrees < -90:
		scale = Vector2(-1,1)
		rotation_degrees = degrees -180
	else:
		scale = Vector2(1,1)
		rotation_degrees = degrees
	
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
#
#
##	action_animation()
#
#func action2():
#	pass
#
#func action_animation():
#	var action_time = 0.2
#	var mod_degrees = 40
#
#	myTween.interpolate_property(item_sprite,"rotation_degrees",0,-mod_degrees/2,action_time*1/4)
#	myTween.interpolate_property(item_sprite,"rotation_degrees",-mod_degrees/2,mod_degrees,action_time*2/4,Tween.TRANS_LINEAR,Tween.EASE_IN,action_time*1/4)
#	myTween.interpolate_property(item_sprite,"rotation_degrees",mod_degrees,0,action_time*1/4,Tween.TRANS_LINEAR,Tween.EASE_IN,action_time*3/4)
#	myTween.start()
#
#func update_item_hand(item_image):
#	var new_item_image = null
#	var new_action_handler = null
#	if item_image:
#		var item_image_path = "res://assets/entity/item/"+item_image.item_name+".png"
#		new_item_image = load(item_image_path)
#
#		var directory = Directory.new()
#		var action_handler_path = "res://prefabs/entity/item/action_handler/"+item_image.item_name+".tscn"
#
#		if directory.file_exists(action_handler_path):
#			new_action_handler = load(action_handler_path)
#		else:
#			new_action_handler = preload("res://prefabs/entity/item/action_handler/generic action_handler.tscn")
#
#
#		$Item.texture = new_item_image
#		item = item_image
#		item_name = item_image.item_name
#
#	else:
#		$Item.texture = new_item_image
#		item = null
#		item_name = null
#
#	var old_action_handler = get_node("Action_handler")
#	if old_action_handler:
#		remove_child(old_action_handler)
#
#	if new_action_handler:
#		new_action_handler = new_action_handler.instance()
#		add_child(new_action_handler)
#		action_handler = new_action_handler
