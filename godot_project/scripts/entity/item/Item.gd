extends Area2D

signal pickup(item)

export var item_name : String setget set_item_name

var item_image 

export var amount = 1 setget set_amount

var is_pickable = false

var body_to_pickup

onready var myTween : = $Tween


func _ready():
	$AnimationPlayer.seek(abs(randf()))
	
	
	velocity = Vector2(rand_range(-40,40),-50)

var velocity = Vector2(40,-50)
var spawn_gravity = Vector2(0,0.4)
var mass = 200

func _process(delta):
		
	if is_pickable:
		if body_to_pickup:
			if position.distance_to(body_to_pickup.position) < 1:
				if body_to_pickup.item_pickup(self):
					emit_signal("pickup",self)
					queue_free()
				else:
					body_to_pickup = null
			else:
				var move_speed = 60
				velocity = (body_to_pickup.position - position).normalized() * move_speed
				translate(velocity*delta)
	else:
		velocity += spawn_gravity * mass * delta
		position += velocity * delta
	
	
func initialize(_position,_item_name, _amount=1):
	self.position=_position
	set_item_name(_item_name)
	set_amount(_amount)

func set_item_name(newName : String):
	item_name = newName
	
	var path = "res://assets/entity/item/{1}.png".format({1:item_name})
	item_image = load(path)
	
	$Image.texture = item_image
	
	
func set_amount(newAmount):
	amount = newAmount
	$Image/Number.text = str(newAmount)

func _on_Item_body_entered(body):
	if body in get_tree().get_nodes_in_group("player"):
		body_to_pickup = body

func _on_Item_body_exited(body):
	if body_to_pickup == body:
		body_to_pickup = null

func _on_Pickup_timer_timeout():
	is_pickable = true




