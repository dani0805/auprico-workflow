# Generated by Django 2.2 on 2019-04-27 15:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Callback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function_name', models.CharField(max_length=200, verbose_name='Name')),
                ('function_module', models.CharField(max_length=400, verbose_name='Module')),
                ('order', models.IntegerField(verbose_name='Order')),
                ('execute_async', models.BooleanField(default=False, verbose_name='Execute Asynchronously')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('condition_type', models.CharField(choices=[('function', 'Function Call'), ('and', 'Boolean AND'), ('or', 'Boolean OR'), ('not', 'Boolean NOT')], max_length=10, verbose_name='Type')),
                ('parent_condition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child_conditions', to='auprico_workflow.Condition', verbose_name='Parent Condition')),
            ],
        ),
        migrations.CreateModel(
            name='CurrentObjectState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.CharField(max_length=200, verbose_name='Object Id')),
                ('updated_ts', models.DateTimeField(auto_now=True, verbose_name='Last Updated')),
            ],
        ),
        migrations.CreateModel(
            name='Function',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('function_name', models.CharField(max_length=200, verbose_name='Function')),
                ('function_module', models.CharField(max_length=400, verbose_name='Module')),
                ('condition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Condition', verbose_name='Condition')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('active', models.BooleanField(verbose_name='Active')),
                ('initial', models.BooleanField(default=False, verbose_name='Initial')),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('label', models.CharField(blank=True, max_length=50, null=True, verbose_name='Label')),
                ('description', models.CharField(blank=True, max_length=400, null=True, verbose_name='Description')),
                ('priority', models.IntegerField(blank=True, null=True, verbose_name='Priority')),
                ('automatic', models.BooleanField(verbose_name='Automatic')),
                ('automatic_delay', models.FloatField(blank=True, null=True, verbose_name='Automatic Delay in Days')),
                ('final_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incoming_transitions', to='auprico_workflow.State', verbose_name='Final State')),
                ('initial_state', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outgoing_transitions', to='auprico_workflow.State', verbose_name='Initial State')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Name')),
                ('object_type', models.CharField(max_length=200, verbose_name='Object_Type')),
                ('initial_prefetch', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Object_Type')),
            ],
        ),
        migrations.CreateModel(
            name='TransitionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(blank=True, null=True, verbose_name='User Id')),
                ('completed_ts', models.DateTimeField(auto_now=True, verbose_name='Time of Completion')),
                ('success', models.BooleanField(verbose_name='Success')),
                ('error_code', models.CharField(blank=True, choices=[('400', '400 - Not Authorized'), ('500', '500 - Internal Error')], max_length=5, null=True, verbose_name='Error Code')),
                ('error_message', models.CharField(blank=True, max_length=4000, null=True, verbose_name='Error Message')),
                ('current_object_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.CurrentObjectState', verbose_name='Object State')),
                ('transition', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Transition', verbose_name='Transition')),
                ('workflow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.CreateModel(
            name='StateVariableDef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='variable_definitions', to='auprico_workflow.State', verbose_name='State')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow')),
            ],
            options={
                'unique_together': {('name', 'workflow', 'state')},
            },
        ),
        migrations.CreateModel(
            name='StateVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('current_object_state', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.CurrentObjectState', verbose_name='Object State')),
                ('state_variable_def', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.StateVariableDef', verbose_name='Variable Definition')),
                ('workflow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.CreateModel(
            name='FunctionParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parameters', to='auprico_workflow.Function', verbose_name='Function')),
                ('workflow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='function',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='currentobjectstate',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.State', verbose_name='State'),
        ),
        migrations.AddField(
            model_name='currentobjectstate',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AddField(
            model_name='condition',
            name='transition',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auprico_workflow.Transition', verbose_name='Transition'),
        ),
        migrations.AddField(
            model_name='condition',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.CreateModel(
            name='CallbackParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('value', models.CharField(max_length=4000, verbose_name='Value')),
                ('callback', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parameters', to='auprico_workflow.Callback', verbose_name='Callback')),
                ('workflow', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='callback',
            name='transition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Transition', verbose_name='Transition'),
        ),
        migrations.AddField(
            model_name='callback',
            name='workflow',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, to='auprico_workflow.Workflow', verbose_name='Workflow'),
        ),
        migrations.AlterUniqueTogether(
            name='transition',
            unique_together={('name', 'final_state')},
        ),
        migrations.AlterUniqueTogether(
            name='state',
            unique_together={('name', 'workflow')},
        ),
        migrations.AddIndex(
            model_name='currentobjectstate',
            index=models.Index(fields=['workflow', 'object_id'], name='auprico_wor_workflo_f8c9f0_idx'),
        ),
    ]
