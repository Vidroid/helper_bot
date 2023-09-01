# !venv/bin/python
import heapq
import random
from datetime import datetime, timedelta
import logging
import re

import networkx as nx

from aiogram.types import CallbackQuery
from apscheduler.triggers.cron import CronTrigger

import conf
import ioF

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher, executor, types

# Объект бота
bot = Bot(token=conf.TOKEN, parse_mode='HTML')
# Диспетчер для бота
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(filename='tbot.log', level=logging.DEBUG)
# logging.basicConfig(level=logging.INFO)
test_chat_users = ioF.read_arr(conf.USERS)
avesta_chat_users = ioF.read_arr('avesta.json')
squad_chat_users = ioF.read_arr('squad.json')

divs = -1001894163066

squad = -1001856769942
print(datetime.now())

G = nx.Graph()
G.add_edges_from(conf.EDGES)


kp = types.InlineKeyboardMarkup()
btn_1 = types.InlineKeyboardButton(text='Иду', callback_data='btn_yep')
btn_2 = types.InlineKeyboardButton(text='Не иду', callback_data='btn_no')
kp.add(btn_1, btn_2)

bosses = {}

if ioF.read_list(conf.BOSSES) == {}:
    bosses = {"5": "Гавгона ", "10": "Пидра ", "15": "Минохуявр ", "20": "Пидармот ",
              "25": "Церебер ", "30": "Тилифон ", "40": "ПирДух Синдара", "50": "Немепидра "}
else:
    bosses = ioF.read_list(conf.BOSSES)

droids = "droids.join"
bosses_d = {}

if ioF.read_list(droids) == {}:
    bosses_d = {"5": "Горгона ", "10": "Гидра ", "15": "Минотавр ", "20": "Пирагмон ",
              "25": "Цербер ", "30": "Тифон ", "40": "Дух Синдара", "50": "Немезида "}
else:
    bosses_d = ioF.read_list(droids)

def get_username(name, user_id):
    return "[" + name + "](tg://user?id=" + str(user_id) + ")"


def stock_helper(msg_text):
    wear = re.findall(r'/give\d{3,}', msg_text)
    potns = re.findall(r'/give_potion_\d{3,}', msg_text)
    resc = re.findall(r'/give_resource_\d{3,}', msg_text)

    print(wear, potns, resc)


async def only_send_msg_to_chat(chat_id, message, chat_users):
    i = 0
    temp = message + ' '
    for user in chat_users:
        #member = await bot.get_chat_member(chat_id, user)

        temp += get_username("котек", user) + ' '
        if i == 4:
            await bot.send_message(chat_id, f"{temp}", parse_mode="Markdown")
            temp = message + ' '
            i = 0
        else:
            i += 1
    if temp != (message + ' '):
        await bot.send_message(chat_id, f"{temp}", parse_mode="Markdown")


@scheduler.scheduled_job(CronTrigger.from_crontab('5,25,45 7-10,12-19,21-23,0-1 * * *'))
async def shed():
    await bot.send_message(conf.CHAT, "⌛<i>️Тик</i>", parse_mode="HTML")
    await bot.send_message(divs, "⌛️<i>Тик</i>", parse_mode="HTML")
    await bot.send_message(squad, "Тик")


async def boss_5lvl_pre():
    await bot.send_message(conf.CHAT, "Босс Горгона появится через 5 минут")


async def boss_5lvl_call():
    await bot.send_message(conf.ME, "Босс Горгона появился")


async def boss_10lvl_pre():
    await bot.send_message(conf.CHAT, "Босс Гидра появится через 5 минут")


async def boss_10lvl_call():
    await bot.send_message(conf.CHAT, "Босс Гидра появился")


async def arena():
    await bot.send_message(conf.CHAT, "Арена открыта для сражений")
    await bot.send_message(divs, "Арена открыта для сражений")
    await bot.send_message(squad, "Арена открыта для сражений")


async def arena_closed():
    await bot.send_message(conf.CHAT, "Арена закрыта")
    await bot.send_message(divs, "Арена закрыта")
    await bot.send_message(squad, "Арена закрыта")


async def battle_start():
    await bot.send_message(conf.CHAT, "Битва на островах началась")
    await bot.send_message(divs, "Битва на островах началась")
    await bot.send_message(squad, "Битва на островах началась")


async def battle_ping():
    msg = await bot.send_message(conf.CHAT, "До битвы на островах осталось 15 минут")
    await bot.send_message(divs, "До битвы на островах осталось 15 минут")
    await bot.send_message(squad, "До битвы на островах осталось 15 минут")
    await only_send_msg_to_chat(conf.CHAT, 'Не спать ', test_chat_users)
    await only_send_msg_to_chat(divs, 'Не спать ', avesta_chat_users)
    await bot.send_message(divs, "<b>Кто идет на чв?</b> \n", parse_mode="HTML", reply_markup=kp)
    await bot.send_message(conf.CHAT, "<b>Кто идет на чв</b>? \n", parse_mode="HTML", reply_markup=kp)



# await only_send_msg_to_chat(squad, 'Не спать ', squad_chat_users)


@scheduler.scheduled_job(CronTrigger.from_crontab('0,20,40 7-10,12-19,21-23,0-1 * * *'))
async def shed_five():
    msg = await bot.send_message(conf.CHAT, "⏳<i>Тик через 5 минут</i>", parse_mode="HTML")
    await bot.send_message(divs, "⏳<i>Тик через 5 минут</i>", parse_mode="HTML")
    await bot.send_message(squad, "Тик через 5 минут")
    # await only_send_msg_to_chat(conf.CHAT, '5 минут до тика', test_chat_users)


def get_username(name, user_id):
    return "[" + name + "](tg://user?id=" + str(user_id) + ")"

    # writing userlist into json file


def get_event_times():
    msg = "📆<b>События на сегодня📆</b>\n"
    war_time_2 = timedelta(hours=20, minutes=0, seconds=0)
    war_time_1 = timedelta(hours=11, minutes=0, seconds=0)
    arena_time = timedelta(hours=16, minutes=0, seconds=0)
    curr = datetime.now()
    check = curr
    check = check - war_time_1
    if curr.day != check.day:
        hr = 10 - curr.hour
        mn = 59 - curr.minute
        sc = 59 - curr.second
        msg += "⛈<b>Утреннее чв начнется через</b><code>" + f' {hr}:{mn}:{sc}' + "\n</code>"

    check = curr
    check -= arena_time
    if curr.day != check.day:
        hr = 15 - curr.hour
        mn = 59 - curr.minute
        sc = 59 - curr.second
        msg += "🏟<b>Арена откроется через</b><code>" + f' {hr}:{mn}:{sc}' + "\n</code>"

    check = curr
    check -= war_time_2
    if curr.day != check.day:
        hr = 19 - curr.hour
        mn = 59 - curr.minute
        sc = 59 - curr.second
        msg += "⛈<b>Вечернее чв начнется через</b><code>" + f' {hr}:{mn}:{sc}</code>'

    else:
        msg += "🔚<b>На сегодня событий больше нет</b>"

    return msg


async def send_and_pin_msg_to_chat(chat_id, message, chat_name, chat_users):
    if message.reply_to_message:
        msg = await bot.send_message(chat_id, message.reply_to_message.text)
        await bot.pin_chat_message(chat_id, msg.message_id)
        # await bot.send_message(conf.PIN, 'Sended and pinned to'+chat_name)
        i = 0
        temp = ''
        for user in chat_users:
            if i < 5:
                temp += get_username('котек ', user)
                await bot.send_message(user, message.reply_to_message.text)
                i += 1
            else:
                await bot.send_message(message.chat.id, f"{temp}", parse_mode="Markdown")
                temp = ''
                i = 0


def build_graph(edges):
    graph = {}
    for src, dest in edges:
        if src not in graph:
            graph[src] = []
        graph[src].append(dest)
    return graph


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor in graph.get(current_node, []):
            distance = current_distance + 1  # Вес всех ребер считаем равными 1
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


graph = conf.EDGES


# Дать список всех вершин, связанных с текущей
# и непосещенных

def get_bound(g, v, path):
    r = []
    for pair, _ in g:
        if (v in pair):
            if v == pair[0]:
                q = pair[1]
            else:
                q = pair[0]
            if not (q in path):
                r.append(q)
    return r


# Генерация всех каркасов графа,
# начинающихся в cтартовой вершине

def all_paths(graph, start, pth, stk, res):
    bounds = get_bound(graph, start, pth)

    if len(bounds) > 0:
        for v in bounds:
            all_paths(graph, v, [v, start] + pth, [v] + stk, res)
    else:
        if len(stk) == 0:
            res.append(pth[-1::-1])
        else:
            all_paths(graph, stk[0], pth, stk[1:], res)
    return res


# Поиск пути в финишную вершину

def search_path(tree, start, fin):
    q = fin
    res = []

    while True:
        k = tree.index(q)
        p = tree[k - 1]

        res = [(p, q)] + res

        if p == start:
            return res

        q = p


# Получить длину пути

def length_path(graph, pth):
    s = 0
    for pair in pth:
        rpair = (pair[1], pair[0])
        s += graph.get(pair, 0) + graph.get(rpair, 0)
    return s


# Парадная программа

def task(graph, start, fin):
    all_pth = all_paths(graph, start, [], [start], [])

    shortest_path = search_path(graph[0], start, fin)
    shortest_len = length_path(graph, shortest_path)

    for pth in all_pth[1:]:

        path = search_path(pth, start, fin)
        length = length_path(graph, path)

        if length < shortest_len:
            shortest_len = length
            shortest_path = path

    return shortest_path, shortest_len


def shortest_path(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []



trig_pairs = ioF.read_list(conf.TRIGS)
trig_pairs["check"] = "done"

trig_avesta = ioF.read_list('avesta_trigs.json')
trig_avesta["check"] = "done"

trig_squad = ioF.read_list('squad_trigs.json')
trig_squad["check"] = "done"

# f_tick_job = scheduler.add_job(shed, "cron", minute=5)
# t_tick_job = scheduler.add_job(shed, "cron", minute=25)
# fh_tick_job = scheduler.add_job(shed, "cron", minute=45)
# z_tick_job = scheduler.add_job(shed_five, "cron", minute=0)
# tz_tick_job = scheduler.add_job(shed_five, "cron", minute=20)
# fz_tick_job = scheduler.add_job(shed_five, "cron", minute=40)

scheduler.add_job(arena, "cron", hour=16)
scheduler.add_job(arena_closed, "cron", hour=17)
scheduler.add_job(battle_ping, "cron", hour=10, minute=45)
scheduler.add_job(battle_start, "cron", hour=11)
scheduler.add_job(battle_ping, "cron", hour=19, minute=45)
scheduler.add_job(battle_start, "cron", hour=20)


@dp.channel_post_handler()
async def chanel_checker(message: types.Message):
    global bosses

    if message.chat.id == -1001340977257:
        # print('olo')

        if message.text.find('🌟 Элитный: Горгона 🎖5 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            await bot.forward_message(divs, -1001340977257, message.message_id)


        if message.text.find('🌟 Элитный: Гидра 🎖10 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            await bot.forward_message(divs, -1001340977257, message.message_id)


        if message.text.find('🌟 Элитный: Минотавр 🎖15 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            await bot.forward_message(divs, -1001340977257, message.message_id)


        if message.text.find('🌟 Элитный: Пирагмон 🎖20 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            await bot.forward_message(divs, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Цербер 🎖25 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Тифон 🎖30 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Дух Синдара 🎖40 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Немезида 🎖50 [Люди] был возрожден вновь!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Горгона 🎖5 [Люди] был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=30, seconds=0)
            bosses[str(5)] = '*Гавгона* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Гидра 🎖10 [Люди] был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=45, seconds=0)
            bosses[str(10)] = '*Пидра* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Минотавр 🎖15 [Люди] был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=60, seconds=0)
            bosses[str(15)] = '*Минохуявр* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Пирагмон 🎖20 [Люди] был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=75, seconds=0)
            bosses[str(20)] = '*Пидармот* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Цербер 🎖25 [Люди] был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=90, seconds=0)
            bosses[str(25)] = '*Церебер* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Тифон 🎖30 был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=120, seconds=0)
            bosses[str(30)] = '*Тилифон* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Дух Синдара 🎖40 был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=120, seconds=0)
            bosses[str(40)] = '*ПирДух Синдара* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Немезида 🎖50 был повержен!') != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            data_msg = message.date + timedelta(minutes=120, seconds=0)
            bosses[str(50)] = '*Немепидра* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find("начал поединок с 🌟 Элитный:") != -1 and message.text.find("[Люди]") != -1:
            await bot.forward_message(conf.CHAT, -1001340977257, message.message_id)
            await bot.forward_message(divs, -1001340977257, message.message_id)
            # if message.text.find("Минотавр") or message.text.find("Пирагмон"):

        await ioF.write_list({}, conf.BOSSES)
        await ioF.write_list(bosses, conf.BOSSES)
        
        if message.text.find('🌟 Элитный: Горгона 🎖5 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Гидра 🎖10 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Минотавр 🎖15 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Пирагмон 🎖20 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Цербер 🎖25 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Тифон 🎖30 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Дух Синдара 🎖40 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Немезида 🎖50 [Дроиды] был возрожден вновь!') != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        if message.text.find('🌟 Элитный: Горгона 🎖5 [Дроиды] был повержен!') != -1:

            data_msg = message.date + timedelta(minutes=30, seconds=0)
            bosses_d[str(5)] = '*Горгона* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Гидра 🎖10 [Дроиды] был повержен!') != -1:

            data_msg = message.date + timedelta(minutes=45, seconds=0)
            bosses_d[str(10)] = '*Гидра* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Минотавр 🎖15 [Дроиды] был повержен!') != -1:

            data_msg = message.date + timedelta(minutes=60, seconds=0)
            bosses_d[str(15)] = '*Минотавр* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Пирагмон 🎖20 [Дроиды] был повержен!') != -1:

            data_msg = message.date + timedelta(minutes=75, seconds=0)
            bosses_d[str(20)] = '*Пирагмон* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'

        if message.text.find('🌟 Элитный: Цербер 🎖25 [Дроиды] был повержен!') != -1:

            data_msg = message.date + timedelta(minutes=90, seconds=0)
            bosses_d[str(25)] = '*Цербер* `' + str(data_msg.day) + "." + str(data_msg.month) + " " + str(
                data_msg.hour) + ':' + str(
                data_msg.minute) + ':' + str(data_msg.second) + '`'


        if message.text.find("начал поединок с 🌟 Элитный:") != -1 and message.text.find("[Дроиды]") != -1:
            await bot.forward_message(squad, -1001340977257, message.message_id)

        await ioF.write_list({}, droids)
        await ioF.write_list(bosses_d, droids)

        # data_msg_full = message.date + datetime.timedelta(minutes=25, seconds=0)
        # data_msg_not_f = message.date + datetime.timedelta(minutes=5, seconds=1)
        # date_msg_fmin = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=1)
        #
        # print(data_msg.hour)
        # if data_msg >= datetime.datetime.now():
        #     if data_msg_not_f < date_msg_fmin:
        #         scheduler.add_job(boss_5lvl_call, "cron", year=data_msg.year, month=data_msg.month,
        #                           day=data_msg.day, week='*', day_of_week='*', hour=data_msg.hour,
        #                           minute=data_msg.minute, second=data_msg.second)
        #         scheduler.add_job(boss_5lvl_pre, "cron", year=data_msg_full.year, month=data_msg_full.month,
        #                           day=data_msg_full.day, week='*', day_of_week='*', hour=data_msg_full.hour,
        #                           minute=data_msg_full.minute, second=data_msg_full.second)
        #         boss_l5 = 'Горгона ' + str(data_msg.hour) + ':' + str(
        #             data_msg.minute) + ':' + str(data_msg.second)
        #         await bot.send_message(conf.CHAT,
        #                                'Босс Горгона будет доступен в ' + str(data_msg.hour) + ':' + str(
        #                                    data_msg.minute) + ':' + str(data_msg.second))
        #
        # else:
        #     scheduler.add_job(boss_5lvl_call, "cron", year=data_msg.year, month=data_msg.month,
        #                       day=data_msg.day, week='*', day_of_week='*', hour=data_msg.hour,
        #                       minute=data_msg.minute, second=data_msg.second)
        #     boss_l5 = 'Горгона ' + str(data_msg.hour) + ':' + str(
        #         data_msg.minute) + ':' + str(data_msg.second)
        #     await bot.send_message(conf.CHAT,
        #                            'Босс Горгона будет доступен в ' + str(data_msg.hour) + ':' + str(
        #                                data_msg.minute) + ':' + str(data_msg.second))
        # data_msg_full = message.date + datetime.timedelta(minutes=40, seconds=0)
        # data_msg_not_f = message.date + datetime.timedelta(minutes=5, seconds=1)
        # date_msg_fmin = datetime.datetime.now() + datetime.timedelta(minutes=5, seconds=1)
        # print(data_msg.hour)
        # if data_msg >= datetime.datetime.now():
        #     if data_msg_not_f < date_msg_fmin:
        #         scheduler.add_job(boss_10lvl_call, "cron", year=data_msg.year, month=data_msg.month,
        #                           day=data_msg.day, week='*', day_of_week='*', hour=data_msg.hour,
        #                           minute=data_msg.minute, second=data_msg.second)
        #         scheduler.add_job(boss_10lvl_pre, "cron", year=data_msg_full.year,
        #                           month=data_msg_full.month,
        #                           day=data_msg_full.day, week='*', day_of_week='*', hour=data_msg_full.hour,
        #                           minute=data_msg_full.minute, second=data_msg_full.second)
        #         boss_l10= 'Гидра ' + str(data_msg.hour) + ':' + str(
        #             data_msg.minute) + ':' + str(data_msg.second)
        #         await bot.send_message(conf.CHAT,
        #                                'Босс Гидра будет доступен в ' + str(data_msg.hour) + ':' + str(
        #                                    data_msg.minute) + ':' + str(data_msg.second))
        # else:
        #     scheduler.add_job(boss_10lvl_call, "cron", year=data_msg.year, month=data_msg.month,
        #                       day=data_msg.day, week='*', day_of_week='*', hour=data_msg.hour,
        #                       minute=data_msg.minute, second=data_msg.second)
        #     boss_l10 = 'Гидра ' + str(data_msg.hour) + ':' + str(
        #         data_msg.minute) + ':' + str(data_msg.second)
        #     await bot.send_message(conf.CHAT,
        #                            'Босс Гидра будет доступен в ' + str(data_msg.hour) + ':' + str(
        #                                data_msg.minute) + ':' + str(data_msg.second))


@dp.message_handler()
async def cmd_test1(message: types.Message):
    logging.debug('into handler')
    tmp = ""
    tm_msg = ""
    boss_timing = "🌟 *Расписание боссов🌟 *\n"

    if message.chat.id == divs:
        if message.text.lower() == 'ебобосы' or message.text.lower() == 'лохи' or message.text.lower() == 'педоры' or message.text.lower() == 'ел':
            for b in bosses.values():
                boss_timing += b + "\n"
            await bot.send_message(divs, boss_timing, parse_mode='Markdown')

        if message.left_chat_member:
            avesta_chat_users.remove(message.left_chat_member.id)
            await ioF.write_list(avesta_chat_users, 'avesta.json')

        if message.text.lower() == "test" and message.from_user.id == conf.ME:

            await bot.send_message(divs, "Кто идет на чв?", reply_markup=kp)
            #await bot.send_message(conf.CHAT, "Кто идет на чв?", reply_markup=kp)

        if ".путь" in message.text.lower():
            temp_str = message.text.replace(".путь ", "")
            await bot.delete_message(message.chat.id, message.message_id)
            path_t = temp_str.split("-")

            res = nx.dijkstra_path(G, path_t[0].lower(), path_t[1].lower())
            answ = "⚔️ <code>Точка:</code><b>" + path_t[1].upper() + "</b> \n\n"
            for v in res:
                answ += "<code>" + str(v) + "→️</code>"
            res = nx.dijkstra_path(G, "бл", path_t[1].lower())
            answ += "\n\n⚔️<b> Путь с базы: </b>\n\n"
            for v in res:
                answ += "<code>" + str(v) + "→️</code>"
            await bot.send_message(divs, answ, parse_mode="HTML")

        if (message.from_user.id == 329383372 or message.from_user.id == conf.ME) and ".пех" in message.text.lower():
            pinned_1 = ioF.read_id("av_pin.json")
            pinned_2 = ioF.read_id("sil_pin.json")

            msg_text = message.text.replace(".пех", "")
            # msg_text = message.text.replace(".Пех", "")
            msg_text = "‼️📡 *\n" + msg_text + "*"
            await bot.delete_message(message.chat.id, message.message_id)
            msg_1 = await bot.send_message(divs, msg_text, parse_mode='Markdown')
            await ioF.write_list(msg_1.message_id, "av_pin.json")
            if pinned_1 != 0:
                try:
                    await bot.delete_message(divs, pinned_1)
                except:
                    print("message is not pinned")
            await bot.pin_chat_message(divs, msg_1.message_id)
            await bot.delete_message(divs, msg_1.message_id + 1)
            msg_2 = await bot.send_message(conf.CHAT, msg_text, parse_mode='Markdown')
            await ioF.write_list(msg_2.message_id, "sil_pin.json")
            if pinned_2 != 0:
                try:
                    await bot.delete_message(conf.CHAT, pinned_2)
                except:
                    print("message is not pinned")
            await bot.pin_chat_message(conf.CHAT, msg_2.message_id)
            await bot.delete_message(conf.CHAT, msg_2.message_id + 1)

        if message.text.lower() == 'события':
            await bot.send_message(divs, get_event_times())

        if message.text.lower() == 'авеста':
            await bot.send_message(divs, "ЪуЪ!")

        if message.text.lower() == 'голас':
            if random.randint(0, 100) < 50:
                await bot.send_message(divs, '🔊🐕*гаў халера*', parse_mode='Markdown')
                await bot.send_message(conf.CHAT, '🔊🐕*гаў халера*', parse_mode='Markdown')
            else:
                await bot.send_message(divs, '🔊🐕*гаў*', parse_mode='Markdown')
                await bot.send_message(conf.CHAT, '🔊🐕*гаў*', parse_mode='Markdown')

        if trig_avesta.get(message.text.lower()) is not None:
            await bot.send_message(divs, trig_avesta[message.text.lower()])

        if message.text.lower().find("t_add ") != -1 and message.reply_to_message:
            if message.reply_to_message.text:
                tmp = message.text
                tmp = tmp.replace("t_add ", "")
                tmp_msg = message.reply_to_message.text
                # print(1)
                trig_avesta[tmp.lower()] = tmp_msg
                await bot.send_message(divs, "added new trigger")

        if message.text.lower().find("t_del ") != -1:
            tmp = message.text
            tmp = tmp.replace("t_del ", "")
            if trig_avesta.get(tmp.lower()) is not None:
                trig_avesta.pop(tmp)
                await bot.send_message(divs, "trigger deleted")
            else:
                await bot.send_message(divs, "trigger not fund")

        if message.from_user.id not in avesta_chat_users:
            avesta_chat_users.append(message.from_user.id)
            await ioF.write_list(avesta_chat_users, 'avesta.json')

        if message.text.lower() == '@all':
            await only_send_msg_to_chat(divs, 'Ало', avesta_chat_users)

        if message.text.find('iamdro') != -1:
            stick = 'CAACAgIAAxkBAAIEM2Td-mPIOhvNNYOFr34tU4YrNOV5AAIOAANEkYcaeGKCpnVCyMYwBA'
            await bot.send_sticker(divs, stick)

        if message.text.lower() == 'trigs':
            tmp = '__Триггеры чата__:\n'
            for pairs in trig_avesta:
                tmp += str(pairs) + '\n'
            await bot.send_message(divs, tmp)
    await ioF.write_list(trig_avesta, 'avesta_trigs.json')


    if message.chat.id == conf.CHAT:
        # print(trig_pairs.get(message.text.lower()) is not None)
        if trig_pairs.get(message.text.lower()) is not None:
            await bot.send_message(conf.CHAT, trig_pairs[message.text.lower()])

        if message.text.lower() == 'события':
            await bot.send_message(conf.CHAT, get_event_times())

        if message.left_chat_member:
            test_chat_users.remove(message.left_chat_member.id)
            await ioF.write_list(test_chat_users, conf.USERS)

        if (message.from_user.id == 400453296 or message.from_user.id == conf.ME) and ".пех" in message.text.lower():
            pinned_1 = ioF.read_id("av_pin.json")
            pinned_2 = ioF.read_id("sil_pin.json")

            msg_text = message.text.replace(".пех", "")
            # msg_text = message.text.replace(".Пех", "")
            msg_text = "‼️📡 *\n" + msg_text + "*"
            await bot.delete_message(message.chat.id, message.message_id)
            msg_1 = await bot.send_message(divs, msg_text, parse_mode='Markdown')
            await ioF.write_list(msg_1.message_id, "av_pin.json")
            if pinned_1 != 0:
                try:
                    await bot.delete_message(divs, pinned_1)
                except:
                    print("message is not pinned")
            await bot.pin_chat_message(divs, msg_1.message_id)
            await bot.delete_message(divs, msg_1.message_id+1)
            msg_2 = await bot.send_message(conf.CHAT, msg_text, parse_mode='Markdown')
            await ioF.write_list(msg_2.message_id, "sil_pin.json")
            if pinned_2 != 0:
                try:
                    await bot.delete_message(conf.CHAT, pinned_2)
                except:
                    print("message is not pinned")
            await bot.pin_chat_message(conf.CHAT, msg_2.message_id)
            await bot.delete_message(conf.CHAT, msg_2.message_id + 1)

        if (message.from_user.id == 400453296 or message.from_user.id == conf.ME) and ".путь" in message.text.lower():
            temp_str = message.text.replace(".путь ", "")
            await bot.delete_message(message.chat.id, message.message_id)
            path_t = temp_str.split("-")
            res = nx.dijkstra_path(G, path_t[0].lower(), path_t[1].lower())
            answ = "⚔️ <code>Точка:</code><b>" + path_t[1].upper() + "</b> \n\n"
            for v in res:
                answ += "<code>" + str(v) + "→</code>️"
            res = nx.dijkstra_path(G, "бл", path_t[1].lower())
            answ += "\n\n⚔️<b> Путь с базы: </b>\n\n"
            for v in res:
                answ += "<code>" + str(v) + "→️</code>"
            await bot.send_message(conf.CHAT, answ, parse_mode="HTML")


        if message.text.lower() == 'голас':
            if random.randint(0, 100) < 50:
                stick = 'CAACAgIAAxkBAAIEM2Td-mPIOhvNNYOFr34tU4YrNOV5AAIOAANEkYcaeGKCpnVCyMYwBA'
                await bot.send_sticker(conf.CHAT, stick)
                await bot.send_message(divs, '🔊🐕*гаў халера*', parse_mode='Markdown')
                await bot.send_message(conf.CHAT, '🔊🐕*гаў халера*', parse_mode='Markdown')
            else:
                await bot.send_message(divs, '🔊🐕*гаў*', parse_mode='Markdown')
                await bot.send_message(conf.CHAT, '🔊🐕*гаў*', parse_mode='Markdown')

        if message.text.lower() == 'ебобосы' or message.text.lower() == 'лохи' or message.text.lower() == 'педоры' or message.text.lower() == 'ел':
            for b in bosses.values():
                boss_timing += b + "\n"
            await bot.send_message(conf.CHAT, boss_timing, parse_mode='Markdown')

        if message.text.lower().find("t_add ") != -1 and message.reply_to_message:
            if message.reply_to_message.text:
                tmp = message.text
                tmp = tmp.replace("t_add ", "")
                tmp_msg = message.reply_to_message.text
                # print(1)
                trig_pairs[tmp] = tmp_msg
                await bot.send_message(conf.CHAT, "added new trigger")

        if message.text.lower().find("t_del ") != -1:
            tmp = message.text
            tmp = tmp.replace("t_del ", "")
            if trig_pairs.get(tmp.lower()) is not None:
                trig_pairs.pop(tmp)
                await bot.send_message(conf.CHAT, "trigger deleted")
            else:
                await bot.send_message(conf.CHAT, "trigger not fund")

        if message.from_user.id not in test_chat_users:
            test_chat_users.append(message.from_user.id)
            await ioF.write_list(test_chat_users, conf.USERS)

        if message.text.lower() == '@all':
            await only_send_msg_to_chat(conf.CHAT, 'Ало', test_chat_users)

        if message.text.lower() == '@frutell1s':
            img = 'AgACAgIAAxkBAAIEMWTd9S3JrHNO63jI9-uhRUZYqIHLAAIG1TEbAAGF8Up0jLyqsBgTpQEAAwIAA3gAAzAE'
            await bot.send_photo(conf.CHAT, img)


        if message.text.lower() == 'trigs':
            tmp = '__Триггеры чата__:\n'
            for pairs in trig_pairs:
                tmp += str(pairs) + '\n'

        if message.text.lower().find('дайтес') != -1 and message.reply_to_message:
            if message.reply_to_message.text:
                admins = ioF.read_arr('asmins.json')
                await only_send_msg_to_chat(conf.CHAT,
                                            'Ало, выдайте со склада __' + message.reply_to_message.text + '__', admins)

        adm = await message.bot.get_chat_member(conf.CHAT, message.from_user.id)
        if message.text.lower() == 'setadm' and message.reply_to_message and adm.status == 'administrator':
            admins = ioF.read_arr('asmins.json')
            if message.reply_to_message.from_user.id not in admins:
                admins.append(message.reply_to_message.from_user.id)
                await ioF.write_list(admins, 'asmins.json')
                await bot.send_message(conf.CHAT, get_username(message.reply_to_message.from_user.full_name,
                                                               message.reply_to_message.from_user.id) + " теперь в списке админов",
                                       parse_mode="Markdown")
            else:
                await bot.send_message(conf.CHAT, "Ты чо, дурной? Он уже в списке")
        elif message.text.lower() == 'setadm' and message.reply_to_message and adm.status != 'administrator':
            await bot.send_message(conf.CHAT, "Cаси жопу ты не админ", )
            
    if message.chat.id == squad:
        if message.text.lower() == 'ебобосы' or message.text.lower() == 'лохи' or message.text.lower() == 'педоры' or message.text.lower() == 'ел':
            for b in bosses_d.values():
                boss_timing += b + "\n"
            await bot.send_message(squad, boss_timing, parse_mode='Markdown')

        if message.left_chat_member:
            squad_chat_users.remove(message.left_chat_member.id)
            await ioF.write_list(squad_chat_users, 'squad.json')

        if message.text.lower() == "test" and message.from_user.id == conf.ME:

            await bot.send_message(squad, "Кто идет на чв?", reply_markup=kp)
            #await bot.send_message(conf.CHAT, "Кто идет на чв?", reply_markup=kp)

        if ".путь" in message.text.lower():
            temp_str = message.text.replace(".путь ", "")
            await bot.delete_message(message.chat.id, message.message_id)
            path_t = temp_str.split("-")

            res = nx.dijkstra_path(G, path_t[0].lower(), path_t[1].lower())
            answ = "⚔️ <code>Точка:</code><b>" + path_t[1].upper() + "</b> \n\n"
            for v in res:
                answ += "<code>" + str(v) + "→️</code>"
            res = nx.dijkstra_path(G, "бл", path_t[1].lower())
            answ += "\n\n⚔️<b> Путь с базы: </b>\n\n"
            for v in res:
                answ += "<code>" + str(v) + "→️</code>"
            await bot.send_message(squad, answ, parse_mode="HTML")


        if message.text.lower() == 'события':
            await bot.send_message(squad, get_event_times())
            
        if message.text.lower() == 'squad0':
            await bot.send_message(squad, "Міць!")

        if message.text.lower() == 'авеста':
            await bot.send_message(squad, "ЪуЪ!")

        if message.text.lower() == 'голас':
            await bot.send_message(squad, '🔊🐕*гаў*', parse_mode='Markdown')

        if trig_squad.get(message.text.lower()) is not None:
            await bot.send_message(squad, trig_avesta[message.text.lower()])

        if message.text.lower().find("t_add ") != -1 and message.reply_to_message:
            if message.reply_to_message.text:
                tmp = message.text
                tmp = tmp.replace("t_add ", "")
                tmp_msg = message.reply_to_message.text
                # print(1)
                trig_squad[tmp.lower()] = tmp_msg
                await bot.send_message(squad, "added new trigger")

        if message.text.lower().find("t_del ") != -1:
            tmp = message.text
            tmp = tmp.replace("t_del ", "")
            if trig_squad.get(tmp.lower()) is not None:
                trig_squad.pop(tmp)
                await bot.send_message(squad, "trigger deleted")
            else:
                await bot.send_message(squad, "trigger not fund")

        if message.from_user.id not in squad_chat_users:
            squad_chat_users.append(message.from_user.id)
            await ioF.write_list(squad_chat_users, 'squad.json')

        if message.text.lower() == '@all':
            await only_send_msg_to_chat(squad, 'Ало', squad_chat_users)

        if message.text.find('iamdro') != -1:
            stick = 'CAACAgIAAxkBAAIEM2Td-mPIOhvNNYOFr34tU4YrNOV5AAIOAANEkYcaeGKCpnVCyMYwBA'
            await bot.send_sticker(squad, stick)

        if message.text.lower() == 'trigs':
            tmp = '__Триггеры чата__:\n'
            for pairs in trig_avesta:
                tmp += str(pairs) + '\n'
            await bot.send_message(squad, tmp)
    await ioF.write_list(trig_squad, 'squad_trigs.json')


    await ioF.write_list(trig_pairs, conf.TRIGS)
    if message.from_user.id == conf.ME:
        if message.text.lower() == 'дайид':
            await bot.send_message(message.chat.id, message.chat.id)

    if message.text.lower() == 'толя':
        await bot.send_message(message.chat.id, 'Пидор!')

    if message.from_user.id == conf.ME:
        if message.text.lower() == 'ало':
            await bot.send_message(message.chat.id, 'who-ем по лбу не дало?')

    if message.text.lower().find("склад_") != -1:
        stock_helper(message.text)


# @dp.message_handler(user_id=conf.ME, content_types=["sticker"])
# async def get_img_id(message):
#     stick_id = message.sticker.file_id
#     await bot.send_message(message.chat.id, f"<b>ИД стикоса:</b>\n{stick_id}")


# @dp.message_handler(user_id=conf.ME, content_types=["photo"])
# async def get_img_id(message):
#     photo_id = message.photo[-1].file_id
#     await bot.send_message(message.chat.id, f"<b>ИД картинки:</b>\n{photo_id}")


@dp.callback_query_handler(lambda call: True)
async def back(callback: CallbackQuery):
    message = callback.message

    if callback.data == 'btn_yep' and callback.from_user.full_name not in message.text:
        await callback.message.edit_text(message.text + "\n" + callback.from_user.full_name, reply_markup=kp)
    else:
        await callback.answer()

    if callback.data == 'btn_no' and callback.from_user.full_name in message.text:
        lst = message.text.split("\n")
        lst.remove(callback.from_user.full_name)
        temp_text = ""
        for item in lst:
            temp_text += item + "\n"
        await callback.message.edit_text(temp_text, reply_markup=kp)
    else:
        await callback.answer()

    await callback.answer()

    #if call.data == 'btn_no':


if __name__ == "__main__":
    # Запуск бота
    logging.debug('into exec')
    scheduler.start()
    executor.start_polling(dp, skip_updates=True)
    logging.debug('outto exec')
