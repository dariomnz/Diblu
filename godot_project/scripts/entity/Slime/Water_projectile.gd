extends Area2D

var attack_damage = 10

onready var myTween : = $Tween

onready var myTimer : = $Death_timer

var direction : Vector2

var velocity = 200

var is_explosion = false
func initialize(_direction,_position,_damage):
	self.position = _position
	self.direction = _direction
	attack_damage = _damage
	
#	print(direction.angle())
	rotation_degrees = rad2deg( direction.angle()) + 90
#	 =.deg2rad()

func _ready():
	myTween.interpolate_property(self,"scale",Vector2(0,0),Vector2(1,1),0.5)
	
	myTween.start()
	
	
func _process(delta):
	if is_explosion:
		if $Death_explosion.emitting == false:
			queue_free()
	else:
		translate(direction * velocity * delta)
	

func _on_Water_projectile_area_entered(area):
	if area.has_method("hit"):
		area.hit(self)

func _on_Death_timer_timeout():
	explosion()
#	queue_free()


func _on_Water_projectile_body_entered(body):
	if not body in get_tree().get_nodes_in_group("player"):
		explosion()
#		queue_free()

func explosion():
	is_explosion = true
	for child in get_children():
		if child == $Death_explosion:
			child.emitting = true
		else:
			child.queue_free()
