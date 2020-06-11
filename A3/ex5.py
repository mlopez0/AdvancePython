from reflect import reflect


@reflect
def myfunction():
    print("nothing\nuseful")


myfunction()


# @reflect on reflect workaround: reflect(reflect) will return decorator reflect with passed argument reflect. 
# Then we call decorator on reflect function.
# It's not possible to apply the reflect decorator againts it owns definition since
# decorators are applied during the definition of the function they are attached to and not 
# during instantiation.
reflect(reflect)(reflect)