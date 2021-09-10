import graphene

from graphene_validator.validation import validate
from .validation_test_suite import InputForTests, OutputForTests, ValidationTestSuite


class ValidatingMutation(graphene.Mutation):
    class Arguments:
        _input = graphene.Argument(InputForTests, name="input")
        root_string = graphene.String()

    Output = OutputForTests

    @classmethod
    def mutate(cls, root, info, **mutation_input):
        validate(cls, root, info, **mutation_input)

        _input = mutation_input.get("_input", {})

        return OutputForTests(
            email=_input.get("email"),
            the_person=_input.get("the_person"),
        )


class Mutations(graphene.ObjectType):
    test_mutation = ValidatingMutation.Field()


class TestMutationValidation(ValidationTestSuite):
    request = """
        mutation Test($input: InputForTests, $rootString: String) {
            testMutation(input: $input, rootString: $rootString) {
                email
                thePerson {
                    theName
                }
            }
        }"""
    schema = graphene.Schema(mutation=Mutations)
