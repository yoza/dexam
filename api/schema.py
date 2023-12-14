import graphene
from graphene_django import DjangoObjectType
from api.models import Recipe

class RecipeType(DjangoObjectType):
    class Meta:
        model = Recipe
        fields = ("id", "name", "description")

    @classmethod
    def get_queryset(cls, queryset, info):
        # Filter out recipes that have no title
        return queryset.exclude(name__exact="")


class Query(graphene.ObjectType):
    """
    Queries for the Recipe model
    """
    recipes = graphene.List(RecipeType)
    recipe_by_name = graphene.Field(RecipeType, name=graphene.String(required=True))

    def resolve_recipes(self, info, **kwargs):
        return Recipe.objects.filter(status=True)

    def resolve_recipe_by_name(root, info, name):
        try:
            return Recipe.objects.get(name=name)
        except Recipe.DoesNotExist:
            return None


class CreateRecipe(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, name, description):
        recipe = Recipe(name=name, description=description)
        recipe.save()
        return CreateRecipe(ok=True, recipe=recipe)


class DeleteRecipe(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    ok = graphene.Boolean()

    def mutate(self, info, id):
        recipe = Recipe.objects.get(id=id)
        recipe.delete()
        return DeleteRecipe(ok=True)


class UpdateRecipe(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()
        description = graphene.String()

    ok = graphene.Boolean()
    recipe = graphene.Field(RecipeType)

    def mutate(self, info, id, name, description):
        recipe = Recipe.objects.get(id=id)
        recipe.name = name
        recipe.description = description
        recipe.save()
        return UpdateRecipe(ok=True, recipe=recipe)


class Mutation(graphene.ObjectType):
    create_recipe = CreateRecipe.Field()
    delete_recipe = DeleteRecipe.Field()
    update_recipe = UpdateRecipe.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
