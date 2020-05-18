from aiohttp import web
from subprocess import call, Popen

if __name__ == "__main__":
    with open('patch_info', 'r') as f:
        d = f.read()
        d = d.split(' ')
        SECRET = d[0]
        PORT = int(d[1])

    proc = None

    async def do_update(request):
        global proc
        if proc: proc.terminate()
        call(['git', 'pull'])
        proc = Popen(['python3', 'n0b0t.py'])
        return web.Response(text='patched and restarted')

    app = web.Application()
    app.router.add_get('/{secret}'.format(secret=SECRET), do_update)
    web.run_app(app, port=PORT)
