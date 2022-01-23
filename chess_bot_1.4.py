import time, random, requests, json

def bestbad(array):
    minIndex = len(array)
    minNumber = 10000
    for i in range(0, len(array)):
         print(array[i][1])
         if (float(array[i][1]) < minNumber):
              minIndex = i
              minNumber = float(array[i][1])
    return array[minIndex][0]

def is_upper(piece):
    if (piece == " "):
        return piece
    else: return piece.upper()

def append_to_jornal(message):
    myfile = open('antihackersBotik_jornal', 'a')
    myfile.write(message + "\n")
    myfile.close()
    print(message)
    return 1

def cost(piece):
    string1 = "QKPRNB "
    string2 = "9015330"
    for i in range(0, 7):
         if (piece.upper() == string1[i]): return int(string2[i])

def what_capture(pos, sq):
    minCost = 10
    for i in range(0, 64):
        if chessmove(pos[i], i, sq, pos):
               whatCost = cost(pos[i])
               if (whatCost < minCost): minCost = whatCost
    return minCost

def my_piece(piece):
   if (move % 2):
       #print(piece, ' ', piece.upper())
       return piece.upper()
   else: 
       #print(piece, ' ', piece.lower())
       return piece.lower()

def add_something(s1, s2):
    global a
    if (a[s1].upper() == "P") and ( (s2 > 55) or (s2 < 8) ): return my_piece("Q")
    return ''

def show_board(board):
    res = ""
    for i in range(0, len(board)):
         if (board[i] == " "):
              res = res + " . "
         else: res = res + " " + board[i] + " "
         if (i % 8 == 7): res = res + "\n"
    append_to_jornal(res)
    return res

def ind(sq):
    a = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(0, len(a)): 
         if (sq[0] == a[i]): p1 = i
    p2 = 8 - int(sq[1])
    return p2 * 8 + p1

def clear_sq(sq):
    global a
    if (sq == "g1"): squares = [ind("h1"), ind("f1")]
    if (sq == "c1"): squares = [ind("a1"), ind("d1")]
    if (sq == "c8"): squares = [ind("a8"), ind("d8")]
    if (sq == "g8"): squares = [ind("h8"), ind("f8")]
    a[squares[1]] = a[squares[0]]
    a[squares[0]] = " "
    return 1


def uncode(uci):
    global a
    our_move = []
    if (len(uci) < 4): 
       print("<4Error")
       return 0
    if (len(uci) == 5):
          sq1 = uci[0] + uci[1]
          sq2 = uci[2] + uci[3]
          piece = uci[4]
          if (move % 2): 
              a[ind(sq2)] = piece.upper()
          else: a[ind(sq2)] = piece.lower()
          a[ind(sq1)] = " "
#          print("pawn-promote ", lastSq)
          return 1
    elif ( (uci[0] + uci[1] == "e1") and ( (uci[2] + uci[3] == "g1") or (uci[2] + uci[3] == "c1") ) )  or  ( (uci[0] + uci[1] == "e8") and ( (uci[2] + uci[3] == "g8") or (uci[2] + uci[3] == "c8") ) ):
          sq1 = uci[0] + uci[1]
          sq2 = uci[2] + uci[3]
          a[ind(sq2)] = a[ind(sq1)]
          a[ind(sq1)] = " "
#          print(sq1, sq2, ": O-O?")
          if (a[ind(sq2)].upper() == "K"): 
               clear_sq(sq2)
          return 1
    elif (len(uci) == 4):
          a[ind(uci[2] + uci[3])] = a[ind(uci[0] + uci[1])]
          a[ind(uci[0] + uci[1])] = " "
#          print("normal-uci", ind(uci[0] + uci[1]), ' ', ind(uci[2] + uci[3]))
          lastSq = 1
          return 1
    else: return 0

def convert(sq):
    a = ["a", "b", "c", "d", "e", "f", "g", "h"]
    return a[sq % 8] + str(int(8 - (sq - (sq % 8)) / 8))

def indexOf(piece, pos):
    for i in range(0, len(pos)):
           if (pos[i] == piece): return i
    return -1

def turn(piece, move):
      if ((piece.upper() == piece) != move): return 0

def chessmove2(piece, pos, sq, b, a):
      if (piece == " "): return 0
      a1 = pos % 8
      a2 = (pos - (pos % 8)) / 8
      sq1 = sq % 8
      sq2 = (sq - (sq % 8)) / 8
      if (turn(piece, testMove % 2) == 0): return 0
#4      if (a[sq] == " ") or ( (a[sq].upper != a[sq]) == move % 2): return 0
      if ((piece != "N") and (piece != "n")):
          if ((sq1 == a1) and (sq2 == a2)): return 0
          if (((sq1 - a1 != 0) and (sq2 - a2 != 0)) and (abs(sq1 - a1) != abs(sq2 - a2))): return 0
          const1 = 0
          const2 = 0
          if (sq1 > a1): const1 = 1
          if (sq1 < a1): const1 = -1 
          if (sq1 == a1): const1 = 0
          if (sq2 > a2): const2 = 1
          if (sq2 < a2): const2 = -1
          if (sq2 == a2): const2 = 0
          if ((piece.upper() == "R") and ((sq1 - a1 != 0) and (sq2 - a2 != 0))): return 0
          if ((piece.upper() == "B") and ((sq1 - a1 == 0) or (sq2 - a2 == 0))): return 0
          if ((piece.upper() == "K") and ((abs(sq1 - a1) > 1) or (abs(sq2 - a2) > 1))): return 0
          if ((piece == "P") and ((abs(sq1 - a1) != 1) or (sq2 - a2 != 1) or (testMove % 2 == 0))): return 0
          if ((piece == "p") and ((abs(sq1 - a1) != 1) or (sq2 - a2 != -1) or (testMove % 2 == 1))): return 0
          a1 = a1 + const1
          a2 = a2 + const2
          while ((a1 != sq1) or (a2 != sq2)):
              if (b[int(a2 * 8 + a1)] != " "): return 0
              a1 = a1 + const1
              a2 = a2 + const2
              if ((a1 < 0) or (a2 < 0) or (a1 > 7) or (a2 > 7)): return 0
          return 1
      else:
          if ((abs(sq1 - a1) > 2) or (abs(sq2 - a2) > 2)): return 0
          if (abs(sq1 - a1) == abs(sq2 - a2)): return 0
          if ((sq1 - a1 == 0) or (sq2 - a2 == 0)): return 0
          return 1

def check_after_move(a, pos, sq):
    global testMove
    b = a.copy()
    testMove = move + 1
    b[sq] = b[pos]
    b[pos] = " "
    if (move % 2):
         king = indexOf("K", b)
    else:
         king = indexOf("k", b)
    for i in range(0, 64):
      if (chessmove2(b[i], i, king, b, a)): return 1
    return 0

def chessmove(piece, pos, sq, a):
      global move
      if (piece == " "): return 0
      a1 = pos % 8
      a2 = (pos - (pos % 8)) / 8
      sq1 = sq % 8
      sq2 = (sq - (sq % 8)) / 8
      if (a[sq] != " "):
           if (turn(a[sq], (move+1) % 2) == 0): return 0 
      if (turn(piece, move % 2) == 0): return 0 
      if (check_after_move(a, pos, sq)): return 0 
      if ((piece != "N") and (piece != "n")):
          if ((sq1 == a1) and (sq2 == a2)): return 0 
          if (((sq1 - a1 != 0) and (sq2 - a2 != 0)) and (abs(sq1 - a1) != abs(sq2 - a2))): return 0 
          const1 = 0
          const2 = 0
          if (sq1 > a1): const1 = 1
          if (sq1 < a1): const1 = -1 
          if (sq1 == a1): const1 = 0
          if (sq2 > a2): const2 = 1
          if (sq2 < a2): const2 = -1
          if (sq2 == a2): const2 = 0
          if ((piece.upper() == "R") and ((sq1 - a1 != 0) and (sq2 - a2 != 0))): return 0 
          if ((piece.upper() == "B") and ((sq1 - a1 == 0) or (sq2 - a2 == 0))): return 0 
          if ((piece.upper() == "K") and ((abs(sq1 - a1) > 1) or (abs(sq2 - a2) > 1))): return 0 
          if ((a[sq] == " ") and (piece.upper() == "P")):
#              if ((piece == "p") and (pos - sq == 16) and (pos > 55) and (pos < 64) and (sq + 8 == " ") and (sq - 1 != "P") and (sq + 1 != "P")): return 1
#              if ((piece == "P") and (sq - pos == 16) and (pos > 7) and (pos < 16) and (sq - 8 == " ") and (sq - 1 != "p") and (sq + 1 != "p")): return 1
              if ((piece == "P") and ((abs(sq1 - a1) > 0) or (sq2 - a2 != 1) or (move % 2 == 0))): return 0 
              if ((piece == "p") and ((abs(sq1 - a1) > 0) or (sq2 - a2 != -1) or (move % 2 == 1))): return 0 
          if ((a[sq] != " ") and (piece.upper() == "P")):
             if ((piece == "P") and ((abs(sq1 - a1) != 1) or (sq2 - a2 != 1) or (move % 2 == 0))): return 0 
             if ((piece == "p") and ((abs(sq1 - a1) != 1) or (sq2 - a2 != -1) or (move % 2 == 1))): return 0 
          while ((a1 != sq1) or (a2 != sq2)):
              a1+=const1
              a2+=const2
              if ((a1 < 0) or (a2 < 0) or (a1 > 7) or (a2 > 7)): return 0 
              if (a[int(a2 * 8 + a1)] != " "): 
                if ((a1 != sq1) or (a2 != sq2)):
                  return 0
          return 1
      else:
          if ((abs(sq1 - a1) > 2) or (abs(sq2 - a2) > 2)): return 0 
          if (abs(sq1 - a1) == abs(sq2 - a2)): return 0 
          if ((sq1 - a1 == 0) or (sq2 - a2 == 0)): return 0 
          return 1

def trans(piece):
        string1 = "QqRrPpBbNnKk "
        string2 = "qQrRpPbBnNkK "
        for i in range(0, 12):
              if (string1[i] == piece): return string2[i]
        return ' '

def variants_of_move(pos):
     n = 0
     for s1 in range(0, 64):
         if (pos[s1] == " "): continue
         for s2 in range(0, 64):
                if (chessmove(pos[s1], s1, s2, pos)): return 1
     return 0

def is_our(piece):
    if (piece == ' '): return 0
    if (piece.upper() == piece):
         return our_color
    else: return (our_color + 1) % 2

def endgame(pos):
    opponent_cost = 0
    for i in range(0, 64):
        if (not is_our(pos[i])): 
#             print(is_upper(pos[i]), ' ', opponent_cost)
             opponent_cost = opponent_cost + cost(is_upper(pos[i]))
    return (opponent_cost < 15)

def our_king(pos):
    for i in range(0, 64):
         if (pos[i].upper() == "K"):
             if (is_our(pos[i])): return i

def protect_attack(pos, sq, sq2):
    global move
    protect_cost = 0
    attack_cost = 0
    for i in range(0, 64):
          if (pos[i] == " "): continue
          if ( chessmove(pos[i], i, sq, pos) ):
#              print("attack: ", i, ' ', sq)
              attack_cost = attack_cost + 1
          else:
              pos2 = pos.copy()
              pos2[sq] = trans(pos[sq])
              move = move + 1
              if ( chessmove2(pos2[i], i, sq, pos2, pos) ): 
#                    print("protect: ", i, ' ', sq)
                    protect_cost = protect_cost + 1
              move = move - 1
    #append_to_jornal(str(protect_cost) + ' ' + str(attack_cost))
    return protect_cost - attack_cost

def two_variants_of_move(pos):
    variants = 0
    what_About_move = ''
    for i1 in range(0, 64):
        if pos[i1] == ' ': continue
        for i2 in range(0, 64):
            if (chessmove(pos[i1], i1, i2, pos)): 
                  variants = variants + 1
                  if (variants == 1): what_About_move = [i1, i2]
                  if (variants == 2): return variants
    if (what_About_move): return what_About_move
    return variants

def one_line_eval(pos):
    global move, calls, spent_time, control, rightMovesArray
    print("SPENT TIME: ", time.time() - spent_time, " CONTROL: ", control)
    if (time.time() - spent_time) > control: 
         calls = calls - 1
         return ''
    calls = calls + 1
    print("CALLS: ", calls)
    if (calls > 3): 
        calls = calls - 1
        return ''
    for i1 in range(0, 64):
        for i2 in range(0, 64):
             if (chessmove(pos[i1], i1, i2, pos)):
                     pos2 = pos.copy()
                     pos2[i2] = pos2[i1]
                     pos2[i1] = ' '
                     move = move + 1
                     v = two_variants_of_move(pos2)
                     if (v == 0) and ( check_after_move(pos2, 0, 0) ): 
                           move = move - 1
                           calls = calls - 1
                           print("CHECKMATE FOUND!!")
                           print("MARK : CHECKMATE IN ", calls+1)
                           rightMovesArray.append(convert(i1) + convert(i2) + add_something(i1, i2))
                           return convert(i1) + convert(i2) + add_something(i1, i2)
                     move = move - 1
                     if (v != 2) and (v != 0):
                         pos2[ v[1] ] = pos2[ v[0] ]
                         pos2[ v[0] ] = ' '
                         if ( one_line_eval(pos2) ): 
                               calls = calls - 1
                               rightMovesArray.append(convert(i1) + convert(i2) + add_something(i1, i2))
                               return convert(i1) + convert(i2) + add_something(i1, i2)
             if (time.time() - spent_time) > control: 
                  calls = calls - 1
                  return ''
    calls = calls - 1
    return ''

def capture(pos, sq):
    for i in range(0, 64):
         if ( chessmove(pos[i], i, sq, pos) ): return 1
    return 0

def freeCheck(pos):
    global move
    for i1 in range(0, 64):
         if pos[i1] == ' ': continue
         for i2 in range(0, 64):
               if (chessmove(pos[i1], i1, i2, pos)):
                       pos2 = pos.copy()
                       pos2[i2] = pos2[i1]
                       pos2[i1] = ' '
                       move = move + 1
                       if ( check_after_move(pos2, 0, 0) and (not capture(pos2, i2) )): 
                              move = move - 1
                              return convert(i1) + convert(i2) + add_something(i1, i2)
                       move = move - 1
    return ''

def FENtranslate(pos, one_const):
        global a, lastSq, move, spent_time
        badmoves = []
        truemoves = []
        if (not pos): return []
        if (one_const) and (not start) and (not lastSq):
             return "Not my move!!!"
        minCost = 10
        cheapConst = 0
        spent_time = time.time()
        if (rightMovesArray):
            ans = rightMovesArray[len(rightMovesArray)-1]
            rightMovesArray.pop(len(rightMovesArray)-1)
            return ans
        Checkmate = one_line_eval(pos)
        if (Checkmate): 
            ans = rightMovesArray[len(rightMovesArray)-1]
            rightMovesArray.pop(len(rightMovesArray)-1)
            return ans
#        free_check = freeCheck(pos)
#        if (free_check): return free_check
        for s1 in range(0, 64):
              if (pos[s1] == " "): continue
              for s2 in range(0, 64):
                    if (chessmove(pos[s1], s1, s2, pos)):
                           if ( (s1 == 13) and (s2 == 21) ) or ( (s1 == 53) and (s2 == 45) ):
                                  badmoves.append([convert(s1) + convert(s2) + add_something(s1, s2), "0.75"])
                                  continue
                           if ( one_const and (s1 == our_king(pos) ) and (not endgame(pos)) and (pos[s2] == ' ')):
                                  badmoves.append([convert(s1) + convert(s2) + add_something(s1, s2), "0.25"])
                                  continue
                           cheap = protect_attack(pos, s2, s1) + 1
                           if (pos[s2] != " "):
                                  if (cost(pos[s1]) - cost(pos[s2]) > 0):
                                          cheap = protect_attack(pos, s2, s1)
                                          append_to_jornal(str(cheap))
#                                          print(cheap, s2)
                                          if (cheap < 0):
                                              cheap = cost(pos[s1])*0.001 - cost(pos[s2])
                                          else: cheap = cost(pos[s1]) - cost(pos[s2])
#                                          print(cheap)
                                  else: cheap = - cost(pos[s2])
                                  if (cheap < minCost):
                                       bestMove = convert(s1) + convert(s2) + add_something(s1, s2)
                                       minCost = cheap
                           else:
                                  move = move + 1
                                  pos2 = pos.copy()
                                  pos2[s2] = pos2[s1]
                                  pos2[s1] = " "
                                  if (cheap <= 0) and ( what_capture(pos2, s2) >= cost(pos2[s2]) ):
                                        cheap = 0
                                  else: cheap = cost(pos[s1])
                                  move = move - 1
#                                  print(cheap, s1, s2)
                           pos2 = pos.copy()
                           pos2[s2] = pos2[s1]
                           pos2[s1] = " "
                           move = move + 1
                           if ((variants_of_move(pos2)) == 0):
                               if (check_after_move(pos2, 0, 0)): return convert(s1) + convert(s2)
                           elif (cheap > 0): 
                               badmoves.append([convert(s1) + convert(s2) + add_something(s1, s2), cheap])
                           else: truemoves.append(convert(s1) + convert(s2) + add_something(s1, s2))
                           move = move - 1
        if (minCost <= cheapConst): 
             print("So we return bestmove ", bestMove)
             return bestMove
        if (not truemoves): 
              append_to_jornal("NOT_TRUE_MOVES!!")
              if (badmoves): return bestbad(badmoves)
              return ""
        return truemoves[random.randint(0, len(truemoves)-1)]

def FENtranslate2(pos):
        global move
        res = []
        for i in range(0, len(pos)):
              if (pos[i] == "/"): continue
              if (pos[i] == " "): 
                   p = pos[i+1]
                   break 
              if (pos[i].isnumeric()):
                   n = int(pos[i])
                   for k in range(0, n): res.append(" ")
              else:
                res.append(trans(pos[i]))
        if (p == "w"):
              move = 0
        else: move = 1
        return res

calls = 0
myfile = open('playstatus', 'r')
accept_const = myfile.read()
myfile.close()
move = 0
testMove = 0
api = "Bearer lip_zKpTlyvdLvjEN85acYGM"
while 1:
 r = requests.get(
    "https://lichess.org/api/stream/event",
    headers = {"Authorization" : api},
    stream = True
 )
 for i in r.iter_lines():
      if (i):
            i = i.decode('utf-8')
            if (json.loads(i).get("type") == "gameStart"):
                      gameId = json.loads(i).get("game").get("id")
                      startPosition = FENtranslate2("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                      break
            if (json.loads(i).get("type") == "challengeDeclined"): continue
            chlId = json.loads(i).get("challenge").get("id")
            opponent = json.loads(i).get("challenge").get("challenger").get("name")
            if ( json.loads(i).get("challenge").get("variant").get("short") != "Std" ):
                if ( json.loads(i).get("challenge").get("variant").get("short") == "FEN" ):
                         startPosition = FENtranslate2(json.loads(i).get("challenge").get("initialFen"))
                         break
                r = requests.post(
                     "https://lichess.org/api/challenge/"+chlId+"/decline",
                     headers = {"Authorization" : api},
                     json = {"reason" : "variant"}
                )
                append_to_jornal("Declined challenge from " + opponent + ": variant")
            else:
                if (not accept_const):
                    r = requests.post(
                     "https://lichess.org/api/challenge/"+chlId+"/decline",
                     headers = {"Authorization" : api},
                     json = {"reason" : "later"}
                    )
                else:
                    control = json.loads(i).get("challenge").get("timeControl").get("limit")
                    if (control):
                        control = control / 60
                    else: control = 30000
                    print("control: ", control)
                    startPosition = FENtranslate2("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                    break
 a = startPosition.copy()
 rightMovesArray = []
 link = "https://lichess.org/api/challenge/"+chlId+"/accept"
 r = requests.post(
    link,
    headers = {"Authorization" : api}
 )
 gameId = chlId
 #print("OK")
 r = requests.get(
    "https://lichess.org/api/bot/game/stream/"+gameId,
     stream = True,
     headers = {"Authorization" : api}
 )
# print(r.status_code)
 append_to_jornal("Antihackers_Botik playing game " + gameId + "..")
 skip = 0
 n = requests.post(
    "https://lichess.org/api/bot/game/"+gameId+"/move/"+FENtranslate(startPosition, 0),
    headers = {"Authorization" : api}
 )
 start = 0
 if (n.status_code == 200):
     append_to_jornal("We are white")
     skip = 1
     start = 1
     our_color = 0
 else: 
     append_to_jornal("We are black")
     our_color = 1
 for i in r.iter_lines():
    if (i):
       if (skip):
           skip = 0
           continue
       lastSq = ""
       a = startPosition.copy()
       move = 0
       #print("OK")
       moves = json.loads(i.decode('utf-8'))
       moves = moves.get("moves")
       if (moves): moves = moves.split(" ")
       #print(moves)
       if moves:
           for i in moves:
                uncode(i)
                move = move + 1
                #print(i, move)
#       show_board(a)
       our_move = FENtranslate(a, 1)
       #print("OK_AY")
       #print(our_move)
       if (not our_move): break
       link = "https://lichess.org/api/bot/game/"+gameId+"/move/"+our_move
       append_to_jornal("We want to move "+ our_move + "..")
       r = requests.post(
            link,
            headers = {"Authorization" : api}
       )
       if (r.status_code == 200): 
              append_to_jornal("Successfully moved " + our_move)
              skip = 1
       else:
           r = requests.post(
               "https://lichess.org/api/bot/game/"+gameId+"/move/e7e5",
               headers = {"Authorization" : api}
           )
           start = 1
 append_to_jornal("Game over")
 myfile = open('playstatus', 'r')
 accept_const = myfile.read()
 myfile.close()