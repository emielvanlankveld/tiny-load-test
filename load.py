import tinify, sys, os, numpy, time, datetime
from PIL import Image
from concurrent import futures
from api_key import API_KEY
tinify.key = API_KEY

def with_concurrent(start):
    count = 0
    with futures.ThreadPoolExecutor(max_workers=50) as executor:
        tasks = dict((executor.submit(handle_request_concurrent, i), i) for i in range(start,start+CYCLE))
        for request in futures.as_completed(tasks):
            count += 1
            print('[{0}] Request {1}{2}'.format(datetime.datetime.now().strftime('%d-%m %H:%M:%S'),start+count,request.result()))
    return start+CYCLE

def handle_request_concurrent(i):
    a = numpy.random.rand(300,300,3) * 255
    image = Image.fromarray(a.astype('uint8')).convert('RGBA')
    name = 'input-python/image{0}.png'.format(str(a[0][0]))
    image.save(name)
    try:
        source = tinify.from_file(name)
        # os.remove(name)
        source.to_file("output-python/output_{0}.png".format(i))
        return ' succeeded. Compression count: {0}'.format(tinify.compression_count)
    except Exception as e:
        return ' failed. {0}'.format(e)

try: limit = sys.argv[1]
except: limit = 0

start_time = time.time()
times = []
CYCLE = 250
start = 0
while start < limit or limit == 0:
    start = with_concurrent(start)
    try: duration = time.time() - (start_time + sum(times))
    except: duration = time.time() - start_time
    times.append(round(duration,1))

    print('This cycle of {0} compressions took {1} seconds. Average so far: {2} seconds | Slowest: {3} seconds | Fastest: {4} seconds'.format(
           CYCLE,
           round(duration,1),
           round(sum(times) / len(times),1),
           max(times),
           min(times)))
