extends Position2D

onready var myTween : = $Tween

var velocity = Vector2(50,-100)
var gravity = Vector2(0,1)
var mass = 200

func initialize(position,text):
	set_text(text)
	
	self.position=position
	velocity = Vector2(rand_range(-50,50),-100)
		
func _ready():
	var max_scale = scale
	scale = Vector2(0,0)
	
	myTween.interpolate_property(self,"modulate",
	Color(modulate.r,modulate.g,modulate.b,modulate.a),
	Color(modulate.r,modulate.g,modulate.b,0.0),
	0.3,Tween.TRANS_LINEAR,Tween.EASE_OUT,0.7)
	
	myTween.interpolate_property(self,"scale",
	Vector2(0,0),
	max_scale,
	0.3,Tween.TRANS_QUART,Tween.EASE_OUT)

	myTween.interpolate_property(self,"scale",
	max_scale,
	Vector2(0.0,0.0),
	1.0,Tween.TRANS_LINEAR,Tween.EASE_OUT,0.6)
	
	myTween.interpolate_callback(self,1.0,"destroy")

	myTween.start()

func _process(delta):
	
	velocity += gravity * mass * delta
	position += velocity * delta
	
func set_text(newText):
	
	$Label.text = str(newText)
	
func get_text():

	return $Label.text
	
func destroy():
	queue_free()
