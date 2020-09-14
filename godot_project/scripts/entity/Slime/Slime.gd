extends KinematicBody2D

const SPEED : int = 60
const SPEED_JUMP : int = 80
const SPEED_DASH : int = 200
const ACCELERATION : int = 250
const FRICTION : int = 200
export (int) var attack_damage : int = 25

enum {
	MOVE,
	DASH,
}

var state = MOVE

var is_inv : bool = false

onready var animationPlayer = $Slime_animation

var velocity = Vector2.ZERO

var dash_vector = Vector2.DOWN
	
func create_jump_smoke():
	var smoke_particle = preload("res://prefabs/particles/Smoke.tscn").instance()
	
	smoke_particle.position = position
	
	get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",smoke_particle)


	
func get_input(delta):
	var input_vector = Vector2.ZERO
	
	input_vector.x = Input.get_action_strength("ui_right") - Input.get_action_strength("ui_left")
	input_vector.y = Input.get_action_strength("ui_down") - Input.get_action_strength("ui_up")
	input_vector = input_vector.normalized()
	
	var is_jump : = false
	if Input.is_action_pressed("ui_space"):
		is_jump = true
	
	if input_vector != Vector2.ZERO:
		# Animacion
		animationPlayer.current_velocity = input_vector
		if is_jump:
			animationPlayer.travel("jump")
		else:
			animationPlayer.travel("run")
		# Movimiento
		dash_vector = velocity.normalized()
#		velocity += input_vector * ACCELERATION * delta
		if animationPlayer.current_node == "jump":
			velocity = velocity.move_toward(input_vector * SPEED_JUMP,ACCELERATION * delta)
#			velocity = velocity.clamped(SPEED_JUMP * delta)
		else:
			velocity = velocity.move_toward(input_vector * SPEED,ACCELERATION * delta)
#			velocity = velocity.clamped(SPEED * delta)
			
		
	else:
		# Animacion
		animationPlayer.travel("idle")
		# Movimiento
		velocity = velocity.move_toward(Vector2.ZERO, FRICTION * delta)
		
		
	if Input.is_action_just_pressed("ui_inventory"):
		if is_inv:
			get_tree().get_nodes_in_group("inventory")[0].close_inv()
			is_inv = false
		else:
			get_tree().get_nodes_in_group("inventory")[0].open_inv()
			is_inv = true
			
	if Input.is_action_pressed("ui_action"):
		if is_in_water():
			get_tree().get_nodes_in_group("inventory")[0].add_item("water")
	
	if Input.is_action_just_pressed("ui_dash"):
			state = DASH
	
#	collision_mask=1
#	collision_layer=1
#	if animationPlayer.current_node == "jump" and can_move:
#		collision_mask=2
#		collision_layer=2
##		aux_speed = speed_jump
#		velocity = input_vector * SPEED_JUMP
#	if animationPlayer.current_node == "run" and can_move:
#		velocity += input_vector * ACCELERATION * delta

func _physics_process(delta):
	match state:
		MOVE:
			move_state(delta)
		DASH:
			dash_state(delta)
	
func move_state(delta):
	get_input(delta)
	move()

func dash_state(_delta):
	velocity = dash_vector * SPEED_DASH
	move()
	animationPlayer.travel("dash")
	
	
func move():
	velocity = move_and_slide(velocity)
	# Para empujar objetos
#	var collision = move_and_collide(velocity)
#	if collision:
#		var collider = collision.collider
#		var remainder = collision.remainder
#
#		if collider in get_tree().get_nodes_in_group("moveables"):
#			collider.move_and_collide(remainder) # move block by remainder
#			collision = move_and_collide(remainder)
	
func dash_animation_finished():
	velocity = velocity/10
	state = MOVE
	
	
func item_pickup(item) ->bool:
	var reminer = get_tree().get_nodes_in_group("inventory")[0].add_item(item.item_name,item.amount)
	
	if reminer == 0:
		return true
	else:
		item.amount = reminer
		return false

func create_water_projectile(_global_position = null,damage = 10):
	var water_item = get_tree().get_nodes_in_group("inventory")[0].get_item("water")
	
	if water_item:
		get_tree().get_nodes_in_group("inventory")[0].remove_amount(water_item,1)
				
		var projectile = preload("res://prefabs/entity/Slime/Water_projectile.tscn").instance()
	
		var direction = global_position.direction_to(get_global_mouse_position())
		
		if not _global_position:
			_global_position = position
		projectile.initialize(direction,_global_position,damage)
		
		get_tree().get_nodes_in_group("world")[0].call_deferred("add_child",projectile)

func is_in_water() -> bool:
	if not get_tree().has_group("Chunk_control"):
		return false
	var chunk = get_tree().get_nodes_in_group("Chunk_control")[0].get_chunk_by_position(position)
	
	if chunk:
		return chunk.is_water(position)
	return false

func _on_HitBox_area_entered(area):
	if area.has_method("hit"):
		area.hit(self)
		
func update_item_hand(item_image : Item_image):
	var generic_item_hand_path = "res://prefabs/entity/item/item_hand/generic.tscn"
	var new_item_hand
		
	if item_image:
		var directory : = Directory.new()
		
		var item_hand_path = "res://prefabs/entity/item/item_hand/"+item_image.item_name+".tscn"
		if directory.file_exists(item_hand_path):
			new_item_hand = load(item_hand_path).instance()
		
		
	if not new_item_hand:
		new_item_hand = load(generic_item_hand_path).instance()
			
	var actual_item_hand = get_node("Item_hand")
	remove_child(actual_item_hand)
	actual_item_hand.queue_free()
	
	if item_image:
		new_item_hand.item_name = item_image.item_name
	else:
		new_item_hand.item_name = null
		
	add_child(new_item_hand)
	
func _hit(hitter : Node2D):
	animationPlayer.travel("hit")
	$"HP bar".number-=hitter.attack_damage
	global.create_float_text(self,hitter.attack_damage)
	
	velocity += hitter.global_position.direction_to(global_position) * global_var.NORMAL_KNOCKBACK/2
