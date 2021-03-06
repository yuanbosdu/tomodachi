#!/usr/bin/env python
import os
import sys
import getopt
import logging
from typing import List, Optional
import tomodachi
from tomodachi.launcher import ServiceLauncher
from tomodachi.watcher import Watcher
from tomodachi.config import parse_config_files


try:
    if ModuleNotFoundError:
        pass
except Exception:
    class ModuleNotFoundError(ImportError):
        pass


class CLI:
    def help_command_usage(self) -> str:
        return ('Usage: tomodachi.py subcommand [options] [args]\n'
                '\n'
                'Options:\n'
                '  -h, --help             show this help message and exit\n'
                '  -v, --version          print tomodachi version\n'
                '  --dependency-versions  print versions of dependencies\n'
                '\n'
                'Available subcommands:\n'
                '  run <service ...> [-c <config-file ...>] [--production]\n'
                '  -c, --config <files>   use json configuration files\n'
                '  -l, --log <level>      specify log level\n'
                '  --production           disable restart on file changes\n'
                )

    def help_command(self) -> None:
        print(self.help_command_usage())
        sys.exit(2)

    def version_command(self) -> None:
        print('tomodachi/{}'.format(tomodachi.__version__))
        sys.exit(0)

    def dependency_versions_command(self) -> None:
        self.test_dependencies(fail_on_errors=False, output_versions=True)
        sys.exit(0)

    def test_dependencies(self, fail_on_errors: bool = True, output_versions: bool = False) -> None:
        errors = False

        try:
            import aiobotocore
            if output_versions:
                print('aiobotocore/{}'.format(aiobotocore.__version__))
        except ModuleNotFoundError as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aiobotocore failed to load (error: "{}")'.format(str(e)))
        except Exception as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aiobotocore failed to load (error: "{}")'.format(str(e)))
            logging.exception('')
            print('')

        try:
            import botocore
            if output_versions:
                print('botocore/{}'.format(botocore.__version__))
        except ModuleNotFoundError as e:  # pragma: no cover
            errors = True
            print('Dependency failure: botocore failed to load (error: "{}")'.format(str(e)))
        except Exception as e:  # pragma: no cover
            errors = True
            print('Dependency failure: botocore failed to load (error: "{}")'.format(str(e)))
            logging.exception('')
            print('')

        try:
            import aiohttp
            if output_versions:
                print('aiohttp/{}'.format(aiohttp.__version__))
        except ModuleNotFoundError as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aiohttp failed to load (error: "{}")'.format(str(e)))
        except Exception as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aiohttp failed to load (error: "{}")'.format(str(e)))
            logging.exception('')
            print('')

        try:
            import aioamqp
            if output_versions:
                print('aioamqp/{}'.format(aioamqp.__version__))
        except ModuleNotFoundError as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aioamqp failed to load (error: "{}")'.format(str(e)))
        except Exception as e:  # pragma: no cover
            errors = True
            print('Dependency failure: aioamqp failed to load (error: "{}")'.format(str(e)))
            logging.exception('')
            print('')

        try:
            # Optional
            import google.protobuf
            if output_versions:
                print('protobuf/{}'.format(google.protobuf.__version__))
        except ModuleNotFoundError as e:  # pragma: no cover
            pass
        except Exception as e:  # pragma: no cover
            pass

        if not errors:
            try:
                import tomodachi.invoker
                import tomodachi.helpers.logging
                import tomodachi.transport.amqp
                import tomodachi.transport.aws_sns_sqs
                import tomodachi.transport.http
                import tomodachi.transport.schedule
            except Exception as e:  # pragma: no cover
                errors = True
                print('Dependency failure: tomodachi essentials failed to load (error: "{}")'.format(str(e)))
                logging.exception('')
                print('')

        if errors:
            if fail_on_errors:
                logging.getLogger('exception').warning('Unable to initialize dependencies')
                logging.getLogger('exception').warning('Error: See above exceptions and traceback')
                sys.exit(1)
            else:
                print('There were errors - see above for exceptions and traceback')

    def run_command_usage(self) -> str:
        return 'Usage: tomodachi.py run <service ...> [-c <config-file ...>] [--production]'

    def run_command(self, args: List[str]) -> None:
        if len(args) == 0:
            print(self.run_command_usage())
        else:
            configuration = None
            log_level = logging.INFO

            if '-c' in args or '--config' in args:
                index = args.index('-c') if '-c' in args else args.index('--config')
                args.pop(index)

                config_files = []  # type: List[str]
                while len(args) > index and args[index][0] != '-':
                    value = args.pop(index)
                    if value not in config_files:
                        config_files.append(value)

                if not len(config_files):
                    print('Missing config file on command line')
                    sys.exit(2)

                try:
                    configuration = parse_config_files(config_files)
                except FileNotFoundError as e:
                    print('Invalid config file: {}'.format(str(e)))
                    sys.exit(2)
                except ValueError as e:
                    print('Invalid config file, invalid JSON format: {}'.format(str(e)))
                    sys.exit(2)

            if '--production' in args:
                index = args.index('--production')
                args.pop(index)
                watcher = None
            else:
                cwd = os.getcwd()
                root_directories = [os.getcwd()]
                for arg in set(args):
                    root_directories.append(os.path.dirname('{}/{}'.format(os.path.realpath(cwd), arg)))
                watcher = Watcher(root=root_directories, configuration=configuration)

            if '-l' in args or '--log' in args:
                index = args.index('-l') if '-l' in args else args.index('--log')
                args.pop(index)
                if len(args) > index:
                    log_level = getattr(logging, args.pop(index).upper(), None) or log_level

            logging.basicConfig(format='%(asctime)s (%(name)s): %(message)s', level=log_level)
            logging.Formatter(fmt='%(asctime)s.%(msecs).03d', datefmt='%Y-%m-%d %H:%M:%S')

            self.test_dependencies()

            ServiceLauncher.run_until_complete(set(args), configuration, watcher)
        sys.exit(0)

    def main(self, argv: List[str]) -> None:
        try:
            opts, args = getopt.getopt(argv, "hlvV ", ['help', 'log', 'version', 'version', 'dependency-versions'])
        except getopt.GetoptError:
            self.help_command()
        for opt, _ in opts:
            if opt in ['-h', '--help']:
                self.help_command()
            if opt in ['-v', '-V', '--version']:
                self.version_command()
            if opt in ['--dependency-versions']:
                self.dependency_versions_command()
        if len(args):
            if args[0] in ('run', 'start', 'go'):
                self.run_command(args[1:])
        self.help_command()


def cli_entrypoint(argv: Optional[List[str]] = None) -> None:
    if argv is None:
        argv = sys.argv
    CLI().main(argv[1:])
