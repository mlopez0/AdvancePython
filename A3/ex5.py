from reflect import reflect

@reflect
def myfunction():
    print("nothing\nuseful")

myfunction()

# Workaround: reflect(reflect) will return decorator reflect with passed argument reflect (What?). 
# Then we call decorator on reflect
# TODO: Add explanation, why it's not possible via simple @reflect
reflect(reflect)(reflect)