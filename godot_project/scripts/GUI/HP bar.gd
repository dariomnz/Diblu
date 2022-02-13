extends HBoxContainer


# Declare member variables here. Examples:
# var a = 2
# var b = "text"
signal death

#var progress_bar : TextureProgress 
#var label_number : Label

export var number : int = 100 setget update_number
export var value_min : int = 0 setget update_min
export var value_max : int = 100 setget update_max


#export var aux_number : int = 100 setget aux_update_number
#export var aux_value_min : int = 0 setget aux_update_min
#export var aux_value_max : int = 100 setget aux_update_max

var myTween : Tween

# Called when the node enters the scene tree for the first time.
func _ready():
#	progress_bar = get_node("Count2/NinePatchRect/Progress_bar")
#	label_number = get_node("Count/Background/Number")
	update_number(number)
	update_max(value_max)
	update_min(value_min)
	
#	myTween = $Tween
#	pass # Replace with function body.

func update_number(newNumber):
	
	var progress_bar = $Count2/NinePatchRect/Progress_bar
	var progress_bar2 = $Count2/NinePatchRect/Progress_bar2
	
	# Comprobacion de los rangos
	if newNumber<=progress_bar.min_value:
		newNumber=progress_bar.min_value
#		emit_signal("death")
	if newNumber>progress_bar.max_value:
		newNumber=progress_bar.max_value
		
	if $Tween.is_inside_tree():
		$Tween.interpolate_method(self,"update_label",number,newNumber,0.25,Tween.TRANS_LINEAR,Tween.EASE_IN,0.1)
		$Tween.interpolate_property(progress_bar,"value",progress_bar.value,newNumber,0.25,Tween.TRANS_LINEAR,Tween.EASE_IN,0.1)
		$Tween.start()
	
	progress_bar2.value = newNumber
	
	if progress_bar2.value<=$Count2/NinePatchRect/Progress_bar2.min_value:
		emit_signal("death")
	
	number=newNumber

func update_label(newText):
	$Count/Background/Number.text=str(int(newText))
	
func update_min(newMin):
	var progress_bar = $Count2/NinePatchRect/Progress_bar
	var progress_bar2 = $Count2/NinePatchRect/Progress_bar2
	value_min=newMin
	progress_bar.min_value=newMin
	progress_bar2.min_value=newMin
	
func update_max(newMax):
	var progress_bar = $Count2/NinePatchRect/Progress_bar
	var progress_bar2 = $Count2/NinePatchRect/Progress_bar2
	value_max=newMax
	progress_bar.max_value=newMax
	progress_bar2.max_value=newMax

	
# Called every frame. 'delta' is the elapsed time since the previous frame.
#func _process(delta):
#	pass


#func _on_Tween_tween_all_completed():
#	if number<=$Count2/NinePatchRect/Progress_bar.min_value:
#		emit_signal("death")
