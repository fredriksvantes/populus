import os
import re
import click
import pytest
from click.testing import CliRunner
from flaky import flaky

from populus.cli import main
from populus.utils.testing import load_contract_fixture


@flaky
@load_contract_fixture('Math.sol')
@load_contract_fixture('WithNoArgumentConstructor.sol')
def test_deployment_command_with_one_specified_contract(project):
    result = runner.invoke(main, ['deploy', 'Math'], input=(
        'testrpc\n'  # select the local chain.
        '0\n'      # select account to deploy from.
        'Y\n'      # write it to config file
    ))

    assert result.exit_code == 0, result.output + str(result.exception)

    # weak assertion but not sure what to do here.
    assert 'Math' in result.output
    assert 'WithNoArgumentConstructor' not in result.output


@flaky
@load_contract_fixture('Math.sol')
@load_contract_fixture('WithNoArgumentConstructor.sol')
@load_contract_fixture('Emitter.sol')
def test_deployment_command_with_specified_contracts(project):
    runner = CliRunner()
    result = runner.invoke(main, [
        'deploy', 'Math', 'Emitter', '--chain', 'testrpc',
    ])

    assert result.exit_code == 0, result.output + str(result.exception)

    # weak assertion but not sure what to do here.
    assert 'Math' in result.output
    assert 'WithNoArgumentConstructor' not in result.output
    assert 'Emitter' in result.output


@flaky
@load_contract_fixture('Math.sol')
@load_contract_fixture('WithNoArgumentConstructor.sol')
@load_contract_fixture('Emitter.sol')
def test_deployment_command_with_prompt_for_contracts(project):
    runner = CliRunner()
    result = runner.invoke(main, [
        'deploy', '--chain', 'testrpc',
    ], input='Math\n')

    assert result.exit_code == 0, result.output + str(result.exception)

    # weak assertion but not sure what to do here.
    assert 'Math' in result.output
    assert 'WithNoArgumentConstructor' in result.output
    assert 'Emitter' in result.output
    assert 'Deploying Math' in result.output
    assert 'Deploying Emitter' not in result.output
    assert 'Deploying WithNoArgumentConstructor' not in result.output
