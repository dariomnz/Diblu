extends KinematicBody2D
class_name Live_entity

signal death(live_entity)

var rand = RandomNumberGenerator.new()

var animationPlayer : AnimationPlayer

var initial_move_speed = 25
var move_speed = 25
var escape_speed = 20
var is_escape_to = null
var can_escape = true
var is_going_to_escape = true

var knockback = Vector2.ZERO

var path : = []
var path_index = 0
var target_point

var wait_time = 0

func _ready():
	rand.randomize()
	for _i in range(0,20):
		var point
		if rand.randi()%2==0:
			point = rand.randf()*2
		else:
			point = Vector2(rand.randi()%150-75+global_position.x,rand.randi()%150-75+global_position.y)
		path.append(point)
		
func _physics_process(delta):
	
	var velocity = Vector2(0,0)
	if is_escape_to and can_escape:
		velocity = (is_escape_to.global_position - global_position).normalized() * escape_speed
		if is_going_to_escape:
			velocity*=-1
		velocity = move_and_slide(velocity)
	else:
		target_point = path[path_index]
		if typeof(target_point) == TYPE_VECTOR2:
			if global_position.distance_to(target_point) < 1:
				change_path_point()
			if typeof(target_point) == TYPE_VECTOR2:
				velocity = (target_point - global_position).normalized() * move_speed
				var collision = move_and_collide(velocity * delta)
				if collision:
					if not collision.collider in get_tree().get_nodes_in_group("player"):
						change_path_point()
		else:
			wait_time+=delta
			if wait_time>target_point:
				wait_time = 0
				change_path_point()
		
	
	knockback = knockback.move_toward(Vector2.ZERO,delta*1500)
	knockback = move_and_slide(knockback)
	
	if velocity != Vector2.ZERO:
		
		animationPlayer.current_velocity = velocity.normalized()

		animationPlayer.travel("run")
	else:
		animationPlayer.travel("idle")
		
		
func change_path_point():
	path_index = wrapi(path_index + 1, 0, path.size())
	target_point = path[path_index]
	move_speed = rand.randi()%initial_move_speed/2+initial_move_speed/2
	
func _hit(hitter : Node2D):
	animationPlayer.travel("hit")
	$"HP bar".number-=hitter.attack_damage
	global.create_float_text(self,hitter.attack_damage)
		
	knockback = hitter.global_position.direction_to(global_position) * global_var.NORMAL_KNOCKBACK


func _on_Vision_area_body_entered(body):
	if body in get_tree().get_nodes_in_group("player"):
		$"Escape timer".stop()
		is_escape_to = body
		change_path_point()


func _on_Vision_area_body_exited(body):
	if $"Escape timer".is_inside_tree():
		if body in get_tree().get_nodes_in_group("player"):
			$"Escape timer".start()


func _on_Escape_timer_timeout():
	is_escape_to = null
	
func _on_HP_bar_death():
	var death_particles = preload("res://prefabs/particles/Death particles.tscn").instance()
	
	death_particles.position = position + Vector2(0,-5)
	
	get_parent().call_deferred("add_child",death_particles)
	
	emit_signal("death",self)
	
	generate_item_loot()
	
	queue_free()

func generate_item_loot():
	"""Method for override"""
	pass
