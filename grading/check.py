import utils
import resource
import subprocess
from pycparser import c_ast

# 512 MiB of memory
BYTES = 512 * 1024 * 1024


def check_ex1():
    output = utils.parse_form('./ex1.txt')
    expected = {'1': 'd', '2': 'c', '3': 'c'}
    grade = 0
    err = 0
    for key in expected.keys():
        out = output.get(key)
        exp = expected.get(key)
        if out is not None:
            if exp == out:
                grade += (20 / 3)
            else:
                err = err + 1
        else:
            err = err + 1
    if err == len(expected):
        return (0, utils.failed('all tests failed... ¯\\_(⊙︿⊙)_/¯'))
    return (grade, utils.passed() if (err == 0) else utils.incomplete('some tests failed... ¯\\_(⊙︿⊙)_/¯'), '')


# checks sum vectorized
def check_ex2():
    try:
        # compile
        utils.make(target='clean')
        task = utils.make(target='sum')
        if task.returncode != 0:
            return (0, utils.failed('compilation error'), task.stderr.decode().strip())
        # run tests
        task = utils.execute(cmd=['./sum'], timeout=15)
        if task.returncode != 0:
            return (0, utils.failed('runtime error'), task.stderr.decode().strip())
        # Output
        output = task.stdout.decode().strip()
        output = list(map(lambda x: float(x.strip().split(':')[1].strip('microseconds').strip()), output.split('\n')[:-1]))
        if output[0] > output[2] and output[1] > output[2]:
            return (50, utils.passed(), '')
        return (0, utils.failed('speedup not achieved...'), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed('TIMEOUT'), '')
    except MemoryError:
        return (0, utils.failed('memory limit exceeded'), '')
    except Exception as e:
        print(e)
        return (0, utils.failed('RESULTADO INESPERADO! Ya probaste ejecutar ./sum?'), '')


# checks sum vectorized unrolled
def check_ex3():
    try:
        # compile
        utils.make(target='clean')
        task = utils.make(target='sum')
        if task.returncode != 0:
            return (0, utils.failed('compilation error'), task.stderr.decode().strip())
        # run tests
        task = utils.execute(cmd=['./sum'], timeout=15)
        if task.returncode != 0:
            return (0, utils.failed('runtime error'), task.stderr.decode().strip())
        # Output
        output = task.stdout.decode().strip()
        output = list(map(lambda x: float(x.strip().split(':')[1].strip('microseconds').strip()), output.split('\n')))
        if output[0] > output[2] and output[1] > output[2] and output[2] > output[3]:
            return (50, utils.passed(), '')
        return (0, utils.failed('speedup not achieved...'), '')
    except subprocess.TimeoutExpired:
        return (0, utils.failed('TIMEOUT'), '')
    except MemoryError:
        return (0, utils.failed('memory limit exceeded'), '')
    except Exception:
        return (0, utils.failed('RESULTADO INESPERADO! Ya probaste ejecutar ./sum?'), '')


def lab10_SIMD():
    not_found = utils.expected_files(['./ex1.txt', './sum.c'])
    if len(not_found) == 0:
        table = []
        ex1_result = check_ex1()
        table.append(('1. Familiarize Yourself', *ex1_result[0: 2]))
        ex2_result = check_ex2()
        table.append(('2. Writing SIMD Code', *ex2_result[0: 2]))
        ex3_result = check_ex3()
        table.append(('3. Loop Unrolling', *ex3_result[0: 2]))
        errors = ''
        errors += utils.create_error('Writing SIMD Code', ex2_result[2])
        errors += '\n' + utils.create_error('Loop Unrolling', ex3_result[2])
        errors = errors.strip()
        grade = 0
        grade += ex1_result[0]
        grade += ex2_result[0]
        grade += ex3_result[0]
        grade = round(grade)
        grade = min(grade, 120)
        report = utils.report(table)
        print(report)
        if errors != '':
            report += '\n\nMore Info:\n\n' + errors
        return utils.write_result(grade, report)
    else:
        utils.write_result(0, 'missing files: %s' % (','.join(not_found)))


if __name__ == '__main__':
    resource.setrlimit(resource.RLIMIT_AS, (BYTES, BYTES))
    lab10_SIMD()
    utils.fix_ownership()
