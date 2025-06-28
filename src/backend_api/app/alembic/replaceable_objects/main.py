from typing import Generic, TypeVar
from alembic.operations import Operations, MigrateOperation

# From Alembic cookbook, with personal additions for typing:
# https://alembic.sqlalchemy.org/en/latest/cookbook.html#replaceable-objects


class ReplaceableObject:
    def __init__(self, name, sqltext):
        self.name = name
        self.sqltext = sqltext


class ReplaceableTrigger(ReplaceableObject):
    def __init__(self, name, table, function, trigger):
        self.name = name
        self.table = table
        self.function = function
        self.trigger = trigger


ObjectType = TypeVar("ObjectType", bound=ReplaceableObject)


class ReversibleOp(MigrateOperation, Generic[ObjectType]):
    def __init__(self, target: ObjectType):
        self.target = target

    @classmethod
    def invoke_for_target(cls, operations: Operations, target: ObjectType):
        op = cls(target)
        return operations.invoke(op)

    def reverse(self):
        raise NotImplementedError()

    @classmethod
    def _get_object_from_version(cls, operations: Operations, ident):
        version, objname = ident.split(".")

        module = operations.get_context().script.get_revision(version).module
        obj = getattr(module, objname)
        return obj

    @classmethod
    def replace(cls, operations: Operations, target, replaces=None, replace_with=None):

        if replaces:
            old_obj = cls._get_object_from_version(operations, replaces)
            drop_old = cls(old_obj).reverse()
            create_new = cls(target)
        elif replace_with:
            old_obj = cls._get_object_from_version(operations, replace_with)
            drop_old = cls(target).reverse()
            create_new = cls(old_obj)
        else:
            raise TypeError("replaces or replace_with is required")

        operations.invoke(drop_old)
        operations.invoke(create_new)


@Operations.register_operation("create_view", "invoke_for_target")
@Operations.register_operation("replace_view", "replace")
class CreateViewOp(ReversibleOp[ReplaceableObject]):
    def reverse(self):
        return DropViewOp(self.target)


@Operations.register_operation("drop_view", "invoke_for_target")
class DropViewOp(ReversibleOp[ReplaceableObject]):
    def reverse(self):
        return CreateViewOp(self.target)


@Operations.register_operation("create_trigger", "invoke_for_target")
@Operations.register_operation("replace_trigger", "replace")
class CreateTriggerOp(ReversibleOp[ReplaceableTrigger]):
    def reverse(self):
        return DropTriggerOp(self.target)


@Operations.register_operation("drop_trigger", "invoke_for_target")
class DropTriggerOp(ReversibleOp[ReplaceableTrigger]):
    def reverse(self):
        return CreateTriggerOp(self.target)


@Operations.implementation_for(CreateViewOp)
def create_view(operations: Operations, operation: CreateViewOp):
    operations.execute(
        "CREATE VIEW %s AS %s" % (operation.target.name, operation.target.sqltext)
    )


@Operations.implementation_for(DropViewOp)
def drop_view(operations: Operations, operation: DropViewOp):
    operations.execute("DROP VIEW %s" % operation.target.name)


@Operations.implementation_for(CreateTriggerOp)
def create_trigger(operations: Operations, operation: CreateTriggerOp):
    operations.execute(
        "CREATE FUNCTION %s() %s" % (operation.target.name, operation.target.function)
    )
    operations.execute(
        "CREATE TRIGGER %s %s" % (operation.target.name, operation.target.trigger)
    )


@Operations.implementation_for(DropTriggerOp)
def drop_trigger(operations: Operations, operation: DropTriggerOp):
    operations.execute(
        "DROP TRIGGER {} ON {};".format(operation.target.name, operation.target.table)
    )
    operations.execute("DROP FUNCTION %s();" % operation.target.name)
