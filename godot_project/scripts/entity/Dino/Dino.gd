extends KinematicBody2D

signal death(dino)

var path : = []
var path_index = 0
var target_point

var valid_point = true

var rand = RandomNumberGenerator.new()

onready var animationPlayer : = $Dino_animation

func _ready():
	rand.seed=randi()
	
	dino_color = dino_colors[randi()%len(dino_colors)]
	
	$Dino_sprite.texture = load("res://assets/entity/dino/"+dino_color+"_Dino.png")
	
	for _i in range(0,20):
		var point
		if rand.randi()%2==0:
			point = rand.randf()*2
		else:
			point = Vector2(rand.randi()%150-75+position.x,rand.randi()%150-75+position.y)
		path.append(point)


var move_speed = 25
var escape_speed = 20
var is_escape_to = null

var wait_time = 0

var dino_colors = ["green","red","blue","yellow"]
var dino_color : String

var knockback = Vector2.ZERO
#var is_death = false

func _physics_process(delta):
	
	var velocity = Vector2(0,0)
	if is_escape_to:
		velocity = (is_escape_to.position - position).normalized() * escape_speed
		velocity*=-1
		velocity = move_and_slide(velocity)
	else:
		target_point = path[path_index]
		if typeof(target_point) == TYPE_VECTOR2:
			if position.distance_to(target_point) < 1:
				change_path_point()
			if typeof(target_point) == TYPE_VECTOR2:
				velocity = (target_point - position).normalized() * move_speed
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
	move_speed = rand.randi()%30+25

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
	
func _hit(hitter : Node2D):
	animationPlayer.travel("hit")
	$"HP bar".number-=hitter.attack_damage
	global.create_float_text(self,hitter.attack_damage)
	
	knockback = hitter.global_position.direction_to(global_position) * global_var.NORMAL_KNOCKBACK
#	if typeof(hitter.velocity) == TYPE_VECTOR2:
#		knockback = hitter.velocity
#	else:
#		knockback = hitter.velocity*hitter.direction
		

func _on_HP_bar_death():
	var death_particles = preload("res://prefabs/particles/Death particles.tscn").instance()
	
	death_particles.position = position + Vector2(0,-5)
	
	get_parent().call_deferred("add_child",death_particles)
	
	emit_signal("death",self)
	
	if rand.randi()%100 <30:
		global.spawn_item(position,dino_color+"_gem")
	else:
		global.spawn_item(position,"bone")
	
	queue_free()
