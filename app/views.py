from django.shortcuts import render, redirect
from django.template import loader
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, date
from django.forms.models import model_to_dict
from django.core import serializers
from .models import *
from .forms import loginForms, signUpForm
# from bson import json_util
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import os
import sys
import json
from django.core import serializers
from django.contrib.auth.hashers import make_password, check_password
import hmac, base64, struct, hashlib, time, requests
from web3 import Web3, HTTPProvider, IPCProvider
from decimal import Decimal
import time
from web3.middleware import ExtraDataToPOAMiddleware
import pandas as pd
from django.db.models import Q
from pyfcm import FCMNotification
from twilio.rest import Client
from django.contrib.auth.hashers import make_password


# 경로 설정
url = os.getenv("WEB3_PROVIDER_URL")
web3 = Web3(Web3.HTTPProvider(url))

# 연결 확인
if web3.is_connected():
    print("Geth IPC 연결 성공!")
else:
    print("Geth IPC 연결 실패.")
web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

tokenContract = web3.eth.contract(abi=[
{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_addr","type":"address"},{"name":"_value","type":"uint256"},{"name":"_release_time","type":"uint256"}],"name":"addTokenLockDate","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[{"name":"_sender","type":"address"}],"name":"lockVolumeAddress","outputs":[{"name":"locked","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[],"name":"note","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_value","type":"uint256"}],"name":"burn","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":False,"inputs":[{"name":"newAdmin","type":"address"}],"name":"setAdmin","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[{"name":"_addr","type":"address"}],"name":"getMinLockedAmount","outputs":[{"name":"locked","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[{"name":"_sender","type":"address"},{"name":"_value","type":"uint256"}],"name":"canTransferIfLocked","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":True,"inputs":[{"name":"_sender","type":"address"}],"name":"LockTransferAddress","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
{"constant":False,"inputs":[{"name":"_addr","type":"address"},{"name":"_value","type":"uint256"}],"name":"addTokenLock","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"},
{"constant":True,"inputs":[],"name":"admin","outputs":[{"name":"","type":"address"}],"payable":False,"stateMutability":"view","type":"function"},{"inputs":[],"payable":False,"stateMutability":"nonpayable","type":"constructor"},
{"payable":True,"stateMutability":"payable","type":"fallback"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"time","type":"uint256"},{"indexed":False,"name":"amount","type":"uint256"}],"name":"AddTokenLockDate","type":"event"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"amount","type":"uint256"}],"name":"AddTokenLock","type":"event"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"burner","type":"address"},{"indexed":False,"name":"amount","type":"uint256"}],"name":"Burn","type":"event"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"previousOwner","type":"address"},{"indexed":True,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},
{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}])

proxy_dict = {
  "http"  : "http://3.39.100.52"
}

# push_service = FCMNotification(api_key="AAAATyxb4sg:APA91bG0Fvva7SyRg8Q6mmVpHw-AHdhQLBDd-MXlVycGm5UMsQEECnQgPoXz9pVUcK95t2gNYqee_HUj6sUwatLGE4cXHbAXJ1tdpaW9ZN7W0PBouKEutlekOzEUdnCdVmYant3OSHe5", proxy_dict=proxy_dict) # 신버전 // 운영기에서 사용

# def sendMessage(ids,title,body):
#   data_message = {
#         "title" :title,
#         "body":body,
#         "show_notification": 'true'
#     }
#   #data payload만 보내야 안드로이드 앱에서 백그라운드/포그라운드 두가지 상황에서 onMessageReceived()가 실행됨
#   result = push_service.single_device_data_message(registration_id=ids, data_message=data_message)

# @csrf_exempt
# def bellsave(request):
#     try:
#         print('알람 저장')
#         userPK = request.POST.get('userPK')
#         solutionStatus = request.POST.get('solutionStatus')
#         savenewStatus = request.POST.get('savenewStatus')
#         userDB = SignUp.objects.get(id = userPK)
#         userDB.solutionPushStatus = solutionStatus
#         userDB.safePushStatus = savenewStatus
#         userDB.save()
#         context = {'value':'1'}
#         return HttpResponse(json.dumps(context))
#     except Exception as error:
#         print(error)
#         context = {'value':'-99'}
#         return HttpResponse(json.dumps(context))


def index(request):
    userinfo = SignUp.objects.all()
    return render(request, 'index.html', {'userinfo':userinfo})




@csrf_exempt
def bellsave(request):
    try:
        print("----------------------------토큰 출금------------------------------")
        # -----------------------------------------------------------------------------
        fromAddr = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'
        toAddr = '0x49b4C5481d33ab4A3ddDb9bF68be0574A4fe02C6'
        # -----------------------------------------------------------------------------
        fromAddrChecksum = web3.to_checksum_address(fromAddr)
        toAddrChecksum = web3.to_checksum_address(toAddr)
        print('       |-----------------(영수증)--------------------|')
        TokenC_I = tokenContract(address=web3.to_checksum_address("0x34bfb68cca8d174192f0e1a63ba3fdf50741ac4e"))
        unRock = web3.geth.personal.unlockAccount(fromAddrChecksum, "asd123!", 10)
        print('          ---------------토큰 집금----------------')
        print('                        unRock: ', unRock)
        test = TokenC_I.functions.transfer(toAddrChecksum, web3.toWei(5000,"ether")).transact({'gas' : 1000000, "from": fromAddrChecksum})
        print('                        토큰 전송 중...')
        print('                        토큰 전송 완료')
        rock = web3.geth.personal.lockAccount(fromAddrChecksum)
        print('                        Rock:   ', rock)
        print('Txn Hash: ',test.hex())
        print('       |---------------------------------------------|')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def bellset(request):
    try:
        print('알람 저장')
        userPK = request.POST.get('userPK')
        userDB = SignUp.objects.get(id = userPK)
        solutionStatus = userDB.solutionPushStatus
        safePushStatus = userDB.safePushStatus
        context = {'value':'1', 'solutionStatus': solutionStatus, 'safePushStatus': safePushStatus}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def tokensava(request):
    try:
        print('토큰 저장')
        userPK = request.POST.get('userPK')
        token = request.POST.get('token')
        userDB = SignUp.objects.get(id = userPK)
        userDB.PushToken = token
        userDB.save()
        print('저-장')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def safenotifi(request):
    try:
        print('뉴스등록 알람')
        sendMessage('e2Q7uopqSxiQOlfOdb4CEA:APA91bHELpvSXdxjtto5BFv7MqgMmX2V3bM1WfOqZl0YnP8w7tHfM028vrciNKAj1lGNyN1qSFYtu3Zh4mWTP90peHIM2wINBJ-9z_sv0S8VYDU4aNjLQFDEW1FmHy29t0maoKvi63Gi', '새로운 안전뉴스가 등록되었습니다.', '지금 바로 확인하세요')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solutionnotifi(request):
    try:
        userPK = request.POST.get('userPK')
        userDB = SignUp.objects.get(id = userPK)
        userToKen = userDB.PushToken
        print('솔루션등록 알람')
        sendMessage(userToKen, '요청하신 솔루션에 대한 답변이 달렸습니다.', '지금 바로 확인하세요')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


@csrf_exempt
def TtoClist(request):
    try:
        userPK = request.POST.get('userPK')
        chlist = (ChangeWallet.objects.filter(userPK = userPK).order_by('-timeStamp'))
        chlist = serializers.serialize('json', chlist)
        test1 = ChangeWallet.objects.filter(userPK = userPK)

        chCount1 = ChangeWallet.objects.filter(status = '1', userPK = userPK).count()
        chCount2 = ChangeWallet.objects.filter(status = '2', userPK = userPK).count()
        print('chCount1: ', chCount1)
        print('chCount2: ', chCount2)
        context = {'value':'1', 'chlist': chlist, 'chCount1': chCount1, 'chCount2': chCount2}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def TtoCsave(request):
    try:
        userPK = request.POST.get('userPK')
        gdsc = request.POST.get('gdsc')
        gdst = request.POST.get('gdst')
        status = request.POST.get('status')
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        userCH = ChangeWallet(
          userPK = userPK,
          gdst = gdst,
          gdsc = gdsc,
          timeStamp = now,
          status = status
        )
        userDB = SignUp.objects.get(id = userPK)
        userGDST = int(userDB.GDSTamount)
        userGDSC = float(userDB.GDSCamount)
        print('userGDST11111: ', userGDST)
        print('userGDSC11111: ', userGDSC)
        userGDST -= int(gdst)
        userGDSC += float(gdsc)
        print('userGDST22222: ', userGDST)
        print('userGDSC22222: ', userGDSC)
        userDB.GDSTamount = userGDST
        userDB.GDSCamount = userGDSC
        userDB.save()
        userCH.save()
        print('------------------GDST -> GDSC 환전 완료------------------')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def CtoTsave(request):
    try:
        userPK = request.POST.get('userPK')
        gdsc = request.POST.get('gdsc')
        gdst = request.POST.get('gdst')
        status = request.POST.get('status')
        now = datetime.now()
        now = now.strftime('%Y-%m-%d %H:%M:%S')

        userCH = ChangeWallet(
          userPK = userPK,
          gdst = gdst,
          gdsc = gdsc,
          timeStamp = now,
          status = status
        )
        userDB = SignUp.objects.get(id = userPK)
        userGDST = int(userDB.GDSTamount)
        userGDSC = float(userDB.GDSCamount)
        print('userGDST11111: ', userGDST)
        print('userGDSC11111: ', userGDSC)
        userGDST += int(gdst)
        userGDSC -= float(gdsc)
        print('userGDST22222: ', userGDST)
        print('userGDSC22222: ', userGDSC)
        userDB.GDSTamount = userGDST
        userDB.GDSCamount = userGDSC
        userDB.save()
        userCH.save()
        print('------------------GDST -> GDSC 환전 완료------------------')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def userEthWallet111(request):
    try:
        Maddr = '0xc1f72d2436f6f23384c2d035e509f795450c2434'
        MaddrCheckSumAddr = web3.to_checksum_address(Maddr)
        moAddr = web3.eth.get_balance(MaddrCheckSumAddr)
        print('moAddr', web3.from_wei(moAddr, 'ether'))
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def userEthWallet1(request):
    try:
        print('잘된다!')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def addrcheck(request):
    try:
        inputAddr = request.POST.get('inputAddr')
        userinfo = SignUp.objects.filter(ethAddr = inputAddr).count()
        print('userinfo: ', userinfo)
        if userinfo == 1:
          context = {'value':'1'}
        elif userinfo == 0:
          context = {'value':'0'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))



@csrf_exempt
def userEthWalletList(request):
    try:
        userPK = request.POST.get('userPK')
        userA = request.POST.get('userA')
        print('userPK: ', userPK)
        print('userA: ', userA)

        userlist = (UserEthWallet.objects.filter(gasUsed = 21000).order_by('-timeStamp'))
        userlist = serializers.serialize('json', userlist)
        fromAdd = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), fromAddr = userA, gasUsed = 21000).count()
        toAdd = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), toAddr = userA, gasUsed = 21000).count()
        countList = fromAdd + toAdd
        print('fromAdd: ', fromAdd)
        print('toAdd: ', toAdd)
        print('fromAdd + toAdd: ',fromAdd + toAdd)
        context = {'value':'1', 'userlist': userlist, 'countList': countList}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def userGdscWalletList(request):
    try:
        userPK = request.POST.get('userPK')
        userA = request.POST.get('userA')
        print('userPK: ', userPK)
        print('userA: ', userA)
        userlist = (UsergdscWallet.objects.filter(tokenSymbol = 'DTR').order_by('-datetime'))
        userlist = serializers.serialize('json', userlist)
        fromAdd = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), fromAddr = userA, tokenSymbol = 'DTR').count()
        toAdd = UsergdscWallet.objects.filter(to = userA, tokenSymbol = 'DTR').count()
        countList = fromAdd + toAdd
        print('fromAdd + toAdd: ',fromAdd + toAdd)
        context = {'value':'1', 'userlist': userlist, 'countList': countList}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def userGDSCWalletSave(request):
    try:
        userPK = request.POST.get('userPK')
        blockHash = request.POST.get('blockHash')
        blockNumber = request.POST.get('blockNumber')
        confirmations = request.POST.get('confirmations')
        cumulativeGasUsed = request.POST.get('cumulativeGasUsed')
        fromAddr = request.POST.get('fromAddr')
        gas = request.POST.get('gas')
        gasPrice = request.POST.get('gasPrice')
        gasUsed = request.POST.get('gasUsed')
        hash = request.POST.get('hash')
        input = request.POST.get('input')
        nonce = request.POST.get('nonce')
        timeStamp = request.POST.get('timeStamp')
        to = request.POST.get('to')
        tokenDecimal = request.POST.get('tokenDecimal')
        tokenName = request.POST.get('tokenName')
        tokenSymbol = request.POST.get('tokenSymbol')
        transactionIndex  = request.POST.get('transactionIndex ')
        value = request.POST.get('value')
        datetime = request.POST.get('datetime')

        moAddr = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'
        freeAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'

        blockCount = UsergdscWallet.objects.filter(blockNumber = blockNumber).count()
        print('blockCount: ', blockCount)
        if blockCount == 0 :
          userinfo = SignUp.objects.get(id = userPK)
          userAddr = userinfo.ethAddr
          userGDSC = float(userinfo.GDSCamount)
          print('유저 GDSC: ', userinfo.GDSCamount)
          print('userAddr 주소는 ?', userAddr)
          print('to 주소는 ?', to)
          print('fromAddr 주소는 ?', fromAddr)
          print('freeAddr 주소는 ?', freeAddr)
          if userAddr == fromAddr:
            if to != moAddr :
              print('출금')
              userGDSC -= float(value)
          elif userAddr.lower() == to :
            if fromAddr != freeAddr :  #수수료 계좌
              print('입금')
              print('입금에 들어옴')
              print('value 값은 : ',value)
              print('userGDSC 값은 :', userGDSC)
              userGDSC += float(value)
          userinfo.GDSCamount = userGDSC
          print('유저 GDSC: ', userinfo.GDSCamount)
          userinfo.save()
          usergdscwallSave = UsergdscWallet(
            userPK = userPK,
            blockHash = blockHash,
            blockNumber = blockNumber,
            confirmations = confirmations,
            cumulativeGasUsed = cumulativeGasUsed,
            fromAddr = fromAddr,
            gas = gas,
            gasPrice = gasPrice,
            gasUsed = gasUsed,
            hash = hash,
            input = input,
            nonce = nonce,
            timeStamp = timeStamp,
            to = to,
            tokenDecimal = tokenDecimal,
            tokenName = tokenName,
            tokenSymbol = tokenSymbol,
            transactionIndex  = transactionIndex ,
            value = value,
            datetime = datetime
          )
          usergdscwallSave.save()
        else:
          print('저장 값 없음')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


@csrf_exempt
def userEthWalletSave(request):
    try:
        userPK = request.POST.get('userPK')
        userAddr = request.POST.get('userAddr')
        fromAddr = request.POST.get('fromAddr')
        toAddr = request.POST.get('to')
        volume = request.POST.get('volume')
        status = request.POST.get('status')
        blockHash = request.POST.get('blockHash')
        blockNumber = request.POST.get('blockNumber')
        confirmations = request.POST.get('confirmations')
        contractAddress = request.POST.get('contractAddress')
        cumulativeGasUsed = request.POST.get('cumulativeGasUsed')
        gas = request.POST.get('gas')
        gasPrice = request.POST.get('gasPrice')
        gasUsed = request.POST.get('gasUsed')
        hash = request.POST.get('hash')
        input = request.POST.get('input')
        isError = request.POST.get('isError')
        nonce = request.POST.get('nonce')
        timeStamp = request.POST.get('timeStamp')
        transactionIndex = request.POST.get('transactionIndex')
        txreceipt_status = request.POST.get('txreceipt_status')
        tokenDecimal = request.POST.get('tokenDecimal')
        tokenName = request.POST.get('tokenName')
        tokenSymbol = request.POST.get('tokenSymbol')

        moAddr = '0x1721DE2111C2061E9a67fB112728897E16705F04'
        freeAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'

        blockCount = UserEthWallet.objects.filter(blockNumber = blockNumber).count()
        if blockCount == 0:
          userinfo = SignUp.objects.get(id = userPK)
          intEth = float(userinfo.ethValue)
          print('intEth: ', intEth)
          if userAddr.lower() == fromAddr.lower() : #유저가 보내는데 받는 사람이 모계좌가 아니면 차감 맞으면 유지 한마디로, 모계좌로 간건 반영 x
            if toAddr.lower() != moAddr.lower() :  # 모계좌
              print('111111111111111111111111111')
              intEth -= float(volume)
          elif userAddr.lower() == toAddr.lower() : #유저가 받는사람이면서 보내는 사람이 수수료 계좌가 아닐땐 증가 맞으면 유지 한마디로, 수수료 받은건 반영 x
            if fromAddr.lower() != freeAddr.lower() :  #수수료 계좌
              print('222222222222222222222222222')
              intEth += float(volume)
          userinfo.ethValue = intEth
          userinfo.save()
          userethwallSave = UserEthWallet(
          userPK = userPK,
          userAddr = userAddr,
          fromAddr = fromAddr,
          toAddr = toAddr,
          eth = volume,
          # submitDate = datetime.now(),
          status = status,
          blockHash = blockHash,
          blockNumber = blockNumber,
          confirmations = confirmations,
          contractAddress = contractAddress,
          cumulativeGasUsed = cumulativeGasUsed,
          gas = gas,
          gasPrice = gasPrice,
          gasUsed = gasUsed,
          hash = hash,
          input = input,
          isError = isError,
          nonce = nonce,
          timeStamp = timeStamp,
          transactionIndex = transactionIndex,
          txreceipt_status = txreceipt_status,
          )
          userethwallSave.save()
        else :
          print('저장 값 없음')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def sendGdsc_transaction(from_address, to_address, value, gas_price, gas, password):
    url = os.getenv("WEB3_PROVIDER_URL")

    #먼저 계정 잠금 해제
    unlock_payload = {
        "jsonrpc" : "2.0",
        "method" : "personal_unlockAccount",
        "params" : [from_address, password, 60],
        "id" : 1
    }

    unlock_response = requests.post(url, json=unlock_payload)
    unlock_result = unlock_response.json()
    print("unlock_result_from_geth : ", unlock_result)
    if unlock_result.get("error"):
        print('unlock Error : ',unlock_result["error"])
    elif unlock_result.get("result") == True :
        print("account unlock success")
    else :
        print("unexpected response", unlock_result)

    value = int(value * (10 ** 18)) 
    data = web3.eth.contract(
        address = "0xe1A7d6838f59965922D01db42D9038402862797A",
        abi = [
            {
                "constant" : False,
                "inputs" : [
                    {
                        "name" : "_to",
                        "type" : "address"
                    },
                    {
                        "name" : "_value",
                        "type" : "uint256"
                    }
                ],
                "name" : "transfer",
                "outputs" : [
                    {
                        "name" : "",
                        "type" : "bool"
                    }
                ],
                "payable" : False,
                "stateMutability" : "nonpayable",
                "type" : "function",   
            }
        ]
    ).encode_abi("transfer", args=[to_address, value])
    #트랜잭션 전송
    nonce = web3.eth.get_transaction_count(from_address, 'pending')
    tx_payload = {
        "jsonrpc" : "2.0",
        "method" : "eth_sendTransaction",
        "params" : [
            {
                "from" : from_address,
                "to" : "0xe1A7d6838f59965922D01db42D9038402862797A",
                "gas" : hex(gas),
                "value" : "0x0",
                "gasPrice" : hex(gas_price),
                "nonce" : hex(nonce),
                "data" : data
            }
        ],
        "id" : 1,
    }
    tx_response = requests.post(url, json=tx_payload)
    tx_result = tx_response.json()
    tx_hash = tx_result.get("result")

    if not tx_hash :
        print("transaction Error", tx_result.get("error"))
        raise Exception("Failed to send transaction. Check transaction parameters.")
    
    return tx_hash


@csrf_exempt
def userSendGDSC(request):
    try:
        userPK = request.POST.get('userPK')
        gdscBalance = request.POST.get('gdscBalance')
        gdscBalance = float(gdscBalance)
        userinfo = SignUp.objects.get(id = userPK)
        userAddr = userinfo.ethAddr
        userGDSC = float(userinfo.GDSCamount)
        print('유저 계좌: ', userAddr)
        print('userGDSC: ', gdscBalance)
        if gdscBalance >= 60.0 :
          print("----------------------------토큰 이체(집금)------------------------------")
          # -----------------------------------------------------------------------------
          gasAddr = "0xf7387cEbDCE62AFBc14A134924323B2337A9A94a"  #수수료 계좌
          fromAddr = userAddr #유저 계좌
          toAddr = "0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6"   #모 계좌
          # -----------------------------------------------------------------------------
          gasCheckSumAddr = web3.to_checksum_address(gasAddr)
          fromAddrChecksum = web3.to_checksum_address(fromAddr)
          toAddrChecksum = web3.to_checksum_address(toAddr)
          uETH = web3.eth.get_balance(fromAddrChecksum)
          getPrice = web3.eth.gas_price
          total = (getPrice * 100000) * 2
        #   sendTx = web3.geth.personal.sendTransaction({            #이체
        #       "from": gasCheckSumAddr,                             #출금 계좌
        #       "gasPrice": getPrice,                                #수수료
        #       "gas": "100000",                                     #Limit Gas
        #       "to": fromAddrChecksum,                              #이체받는 계좌
        #       "value": total,                                      #입금갯수
        #       "data": ""                                           #data
        #   }, 'asd123!')
          tx_hash = send_transaction(gasCheckSumAddr, fromAddrChecksum, total, getPrice, 21000, 'asd123!')
          print('eth수수료 전송 tx_hash : ',tx_hash)
          print('수수료 계좌:   ', gasCheckSumAddr)
          print('받는 계좌:     ', fromAddrChecksum)
          print('모 계좌:       ', toAddrChecksum)
          print('받는 계좌 잔액: ', web3.from_wei(uETH, 'ether'))
          print('수수료 이체중...')
          time.sleep(20)
          uETH1 = web3.eth.get_balance(fromAddrChecksum)
          print('받는 계좌 잔액: ', web3.from_wei(uETH1, 'ether'))
          print('       |-----------------(영수증)--------------------|')
          print('            수수료 입금:    ', web3.from_wei(total, 'ether'))
        #   TokenC_I = tokenContract(address=web3.to_checksum_address("0x34bfb68cca8d174192f0e1a63ba3fdf50741ac4e"))
        #   unRock = web3.geth.personal.unlockAccount(fromAddrChecksum, "asd123!", 10)
          print('          ---------------토큰 집금----------------')
        #   print('                        unRock: ', unRock)
          gdsc_tx_hash = sendGdsc_transaction(fromAddrChecksum, toAddrChecksum, gdscBalance, getPrice, 60000, 'asd123!')
        #   test = TokenC_I.functions.transfer(toAddrChecksum, web3.toWei(gdscBalance,"ether")).transact({'gas' : 100000, "from": fromAddrChecksum})
          print('                        토큰 전송 중...')
          print('                        토큰 전송 완료')
        #   rock = web3.geth.personal.lockAccount(fromAddrChecksum)
        #   print('                        Rock:   ', rock)
          print('       |---------------------------------------------|')
          print('gdsc 전송 tx_Hash: ',gdsc_tx_hash)
          print("----------------------------------------------------------------------")
        else :
          print('GDSC150개 미만 집금X')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


# 새로운 계정 생성 (personal_newAccount)
def create_new_account(password):
    url = os.getenv("WEB3_PROVIDER_URL")
    payload = {
        "jsonrpc": "2.0",
        "method": "personal_newAccount",
        "params": [password],
        "id": 1
    }
    response = requests.post(url, json=payload)
    return response.json().get("result")  # 계정 주소만 반환

@csrf_exempt
def newAccount(request):
    try:
        url = os.getenv("WEB3_PROVIDER_URL")
        web3 = Web3(Web3.HTTPProvider(url))
        print("-----------------------------계좌 생성--------------------------------")
        print("web3 - Connection : ", web3.is_connected())
        userID = request.POST.get('userID')
        addr = create_new_account('asd123!')
        print('addr: ', addr)
        userinfo = SignUp.objects.get(id = userID)
        # userinfo.walletMakeTime = datetime.now() + datetime.timedelta(hours=9)
        userinfo.ethAddr = addr
        userinfo.save()
        print(userinfo.username + " 님 유저 계좌 생성 완료 : " + addr)
        print("----------------------------------------------------------------------")
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def gdscWithdraw(request):
    try:
        userPK = request.POST.get('userPK')
        userAddr = request.POST.get('userAddr')
        toAddr = request.POST.get('to')
        volume = request.POST.get('volume')
        userinfo = SignUp.objects.filter(ethAddr = toAddr).count()
        user = SignUp.objects.get(id = userPK)
        print('userAddruserAddruserAddruserAddruserAddr:', userAddr)
        if userinfo == 1 :                                  #App유저 에게 이체
          volume = float(volume)
          if float(user.GDSCamount) >= volume :
            userTo = SignUp.objects.get(ethAddr = toAddr)
            intGDSCto = float(userTo.GDSCamount)
            intETHto = float(userTo.ethValue)
            intETHto -= 0.005
            userTo.ethValue = intETHto
            print('intETHto: ', intETHto)
            print('intGDSCto: ', intGDSCto)
            intGDSCto1 = float(volume) + intGDSCto
            print('intGDSCto1: ', intGDSCto1)
            userTo.GDSCamount = str(intGDSCto1)
            print('userTo.GDSCamount: ', userTo.GDSCamount)
            user = SignUp.objects.get(id = userPK)
            intEth = float(user.GDSCamount)
            intEth1 = intEth - float(volume)
            user.GDSCamount = str(intEth1)
            print('user.GDSCamount: ', user.GDSCamount)
            user.GDSCamount = str(intEth1)
            intEthh = float(user.ethValue)
            intEthh1 = intEthh - 0.005
            user.ethValue = str(intEthh1)
            user.save()
            user.save()
            userTo.save()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            usergdscwallSave = UsergdscWallet(
              userPK = userPK,
              blockHash = None,
              blockNumber = None,
              confirmations = None,
              cumulativeGasUsed = None,
              fromAddr = userAddr,
              gas = None,
              gasPrice = 0.005,
              gasUsed = None,
              hash = None,
              input = None,
              nonce = None,
              timeStamp = None,
              to = toAddr,
              tokenDecimal = None,
              tokenName = 'abcd',
              tokenSymbol = 'DTR',
              transactionIndex = None,
              value = volume,
              datetime = now,
            )
            usergdscwallSave.save()
        elif userinfo == 0:                                 #외부계좌 출금
          volume = float(volume)
          if float(user.GDSCamount) >= volume :
            print("----------------------------토큰 출금------------------------------")
            # -----------------------------------------------------------------------------
            gasAddr = "0xf7387cEbDCE62AFBc14A134924323B2337A9A94a"
            fromAddr = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'
            toAddr = toAddr
            # -----------------------------------------------------------------------------
            gasCheckSumAddr = web3.to_checksum_address(gasAddr)
            fromAddrChecksum = web3.to_checksum_address(fromAddr)
            toAddrChecksum = web3.to_checksum_address(toAddr)
            getPrice = web3.eth.gas_price
            uETH = web3.eth.get_balance(fromAddrChecksum)
            total = (getPrice * 100000) * 2
            tx_hash = send_transaction(gasCheckSumAddr, fromAddrChecksum, total, getPrice, 21000, 'asd123!')
            print('eth수수료 전송 tx_hash : ',tx_hash)
            print('수수료 계좌:   ', gasCheckSumAddr)
            print('받는 계좌:     ', fromAddrChecksum)
            print('받는 계좌 잔액: ', web3.from_wei(uETH, 'ether'))
            print('수수료 이체중...')
            time.sleep(20)
            print('       |-----------------(영수증)--------------------|')
            # TokenC_I = tokenContract(address=web3.to_checksum_address("0x34bfb68cca8d174192f0e1a63ba3fdf50741ac4e"))
            print('            수수료 입금:    ', web3.from_wei(total, 'ether'))
            # unRock = web3.geth.personal.unlockAccount(fromAddrChecksum, "asd123!", 10)
            print('          ---------------토큰 집금----------------')
            # print('                        unRock: ', unRock)
            gdsc_tx_hash = sendGdsc_transaction(fromAddrChecksum, toAddrChecksum, volume, getPrice, 60000, 'asd123!')
            # test = TokenC_I.functions.transfer(toAddrChecksum, web3.toWei(volume,"ether")).transact({'gas' : 100000, "from": fromAddrChecksum})
            print('                        토큰 전송 중...')
            print('                        토큰 전송 완료')
            # rock = web3.geth.personal.lockAccount(fromAddrChecksum)
            # print('                        Rock:   ', rock)
            print('       |---------------------------------------------|')
            print('gdsc 전송 tx_Hash: ',gdsc_tx_hash)
            print("----------------------------------------------------------------------")
            user = SignUp.objects.get(id = userPK)
            intEth = float(user.GDSCamount)
            intEth1 = intEth - volume
            user.GDSCamount = str(intEth1)
            intEthh = float(user.ethValue)
            intEthh1 = intEthh - 0.005
            user.ethValue = str(intEthh1)
            user.save()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            usergdscwallSave = UsergdscWallet(
              userPK = userPK,
              blockHash = None,
              blockNumber = None,
              confirmations = None,
              cumulativeGasUsed = None,
              fromAddr = userAddr,
              gas = None,
              gasPrice = 0.005,
              gasUsed = None,
              hash = None,
              input = None,
              nonce = None,
              timeStamp = None,
              to = toAddr,
              tokenDecimal = None,
              tokenName = 'abcd',
              tokenSymbol = 'DTR',
              transactionIndex = None,
              value = volume,
              datetime = now,
            )
            usergdscwallSave.save()
            print("-------------------------------------------------------------------")
          else :
            print('float(user.GDSCamount): ', float(user.GDSCamount))
            print('volume: ', volume)
            print('결괴: ', float(user.GDSCamount) >= volume)
            print('안됨')
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

def unlock_account(address, password, duration=60):
    url = os.getenv("WEB3_PROVIDER_URL")  # Geth의 JSON-RPC URL
    payload = {
        "jsonrpc": "2.0",
        "method": "personal_unlockAccount",
        "params": [address, password, duration],  # 주소, 비밀번호, 유지 시간(초 단위)
        "id": 1
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    # 결과 확인
    if result.get("error"):
        print("Unlock Error:", result["error"])  # 오류 메시지 출력
        return False
    elif result.get("result") == True:
        print("Account unlocked successfully!")
        return True
    else:
        print("Unexpected response:", result)
        return False

@csrf_exempt
def ethWithdraw(request):
    try:
        userPK = request.POST.get('userPK')
        userAddr = request.POST.get('userAddr')
        toAddr = request.POST.get('to')
        inputAddr = request.POST.get('inputAddr')
        volume = request.POST.get('volume')
        EXethValue = request.POST.get('EXethValue')

        userinfo = SignUp.objects.filter(ethAddr = inputAddr).count()
        if userinfo == 1: #내부면
            userTo = SignUp.objects.get(ethAddr = inputAddr)
            intEthTo = float(userTo.ethValue)
            print('intEthTo: ', intEthTo)
            intEthTo1 = float(volume) + intEthTo
            print('intEthTo1: ', intEthTo1)
            userTo.ethValue = str(intEthTo1)
            print('userTo.ethValue: ', userTo.ethValue)
            user = SignUp.objects.get(id = userPK)
            intEth = float(user.ethValue)
            intEth1 = intEth - float(EXethValue)
            user.ethValue = str(intEth1)
            user.save()
            userTo.save()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            userethwallSave = UserEthWallet(
              userPK = userPK,
              userAddr = userAddr,
              fromAddr = userAddr,
              toAddr = toAddr,
              eth = volume,
              # submitDate = datetime.now(),
              status = None,
              blockHash = None,
              blockNumber = None,
              confirmations = None,
              contractAddress = None,
              cumulativeGasUsed = None,
              gas = None,
              gasPrice = None,
              gasUsed = 21000,
              hash = None,
              input = None,
              isError = None,
              nonce = None,
              timeStamp = now,
              transactionIndex = None,
              txreceipt_status = None,
            )
            print('intEth: ',intEth)
            print('intEth1: ',intEth1)
            print('EXethValue: ', EXethValue)
            print('userPK: ',userPK)
            print('userAddr: ',userAddr)
            print('toAddr: ',toAddr)
            print('volume: ',volume)
            print('datetime.now(): ', now)
            userethwallSave.save()
        elif userinfo == 0: #외부면
            print("------------------------------출금--------------------------------")
            Maddr = '0x1721DE2111C2061E9a67fB112728897E16705F04'  #모계좌
            Uaddr = inputAddr  #유저가 입력한 계좌
            MaddrCheckSumAddr = web3.to_checksum_address(Maddr)
            UaddrCheckSumAddr = web3.to_checksum_address(Uaddr)
            moAddr = web3.eth.get_balance(MaddrCheckSumAddr)
            getPrice = web3.eth.gas_price
            addrEth = float(EXethValue) * 1000000000000000000
            addrEth = int(addrEth)
            addrEth = int(addrEth - 20000000000000000)
            totalGas = int(getPrice * 21000)
            tx_hash = send_transaction(MaddrCheckSumAddr, UaddrCheckSumAddr, addrEth, getPrice, 21000, 'asd123!')
            # sendTx = web3.geth.personal.sendTransaction({
            #     "from": MaddrCheckSumAddr,
            #     "gasPrice": getPrice,
            #     "gas": "21000",
            #     "to": UaddrCheckSumAddr,
            #     "value": addrEth,
            #     "data": ""
            # }, 'asd123!')
            print('txhash',tx_hash)
            print('모 계좌:     ', Maddr)
            print('받는 계좌:   ', Uaddr)
            print('       |------------------(영수증)-------------------|')
            print('             모 계좌 잔액:     ', web3.from_wei(moAddr, 'ether'))
            print('             보내는 금액:      ', web3.from_wei(addrEth, 'ether'))
            print('                    ++++++++++++++++++++++')
            print('             가스비:           ', web3.from_wei(totalGas, 'ether'))
            print('       |---------------------------------------------|')

            user = SignUp.objects.get(id = userPK)
            intEth = float(user.ethValue)
            intEth1 = intEth - float(EXethValue)
            user.ethValue = str(intEth1)
            user.save()
            now = datetime.now()
            now = now.strftime('%Y-%m-%d %H:%M:%S')
            userethwallSave = UserEthWallet(
              userPK = userPK,
              userAddr = userAddr,
              fromAddr = userAddr,
              toAddr = toAddr,
              eth = volume,
              # submitDate = datetime.now(),
              status = None,
              blockHash = None,
              blockNumber = None,
              confirmations = None,
              contractAddress = None,
              cumulativeGasUsed = None,
              gas = None,
              gasPrice = None,
              gasUsed = 21000,
              hash = None,
              input = None,
              isError = None,
              nonce = None,
              timeStamp = now,
              transactionIndex = None,
              txreceipt_status = None,
            )
            userethwallSave.save()
            print("-----------------------------------------------------------------")
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

def send_transaction(from_address, to_address, value, gas_price, gas, password):
    url = os.getenv("WEB3_PROVIDER_URL")
    
    # 1. 계정을 잠금 해제
    unlock_payload = {
        "jsonrpc": "2.0",
        "method": "personal_unlockAccount",
        "params": [from_address, password, 60],  # 60초 동안 잠금 해제 유지
        "id": 1
    }
    unlock_response = requests.post(url, json=unlock_payload)
    unlock_result = unlock_response.json()
    if unlock_result.get("error"):
        print("Unlock Error:", unlock_result["error"])  # 오류 메시지 출력
    elif unlock_result.get("result") == True:
        print("Account unlocked successfully!")
    else:
        print("Unexpected response:", unlock_result)
    
    # 2. 트랜잭션 전송
    nonce = web3.eth.get_transaction_count(from_address, 'pending')
    tx_payload = {
        "jsonrpc": "2.0",
        "method": "eth_sendTransaction",
        "params": [{
            "from": from_address,
            "to": to_address,
            "value": hex(value),  # Wei 단위로 value 전달, hex로 변환 필요
            "gasPrice": hex(gas_price),  # 가스 가격도 hex로 변환
            "gas": hex(gas),  # 가스 양도 hex로 변환
            "nonce": hex(nonce),  # 명시적으로 nonce를 설정
            "data": "0x"  # 빈 데이터를 hex로 전달
        }],
        "id": 2
    }
    tx_response = requests.post(url, json=tx_payload)
    tx_result = tx_response.json()
    tx_hash = tx_result.get("result")
    
    if not tx_hash:
        print("Transaction Error:", tx_result.get("error"))  # 오류 메시지 출력
        raise Exception("Failed to send transaction. Check transaction parameters.")
    
    return tx_hash

@csrf_exempt
def allAmount(request):
    userId = request.POST.get("userPK")
    if not userId:
        print("Error: userPK is missing in the POST data.")
        return HttpResponse(status=400, content="UserPK is missing")

    try:
        userinfo = SignUp.objects.get(id=userId)
    except SignUp.DoesNotExist:
        print(f"Error: No user found with username {userId}")
        return HttpResponse(status=404, content="User not found")

    if not web3.is_connected():
        print("Error: Not connected to Geth node.")
        return HttpResponse(status=500, content="Geth connection error")

    try:
        userAddr = userinfo.ethAddr
        bal = web3.eth.get_balance(userAddr)
        print('Balance in wei:', bal)  # wei 단위로 확인
        eth_balance = web3.from_wei(bal, 'ether')
        print('Balance in ether:', eth_balance)  # ether 단위로 확인
        userinfo.ethValue = eth_balance  # 필요한 경우 정수 변환
        userinfo.save()
    except Exception as e:
        print("Error while fetching balance or saving:", str(e))
        return HttpResponse(status=500, content="Balance fetch or save error")

    print('----------------------allAmount--------------')
    print('allAmount 요청 받음 전달할 bal값은', str(eth_balance))
    context = {'value': str(eth_balance)}
    return HttpResponse(json.dumps(context))




@csrf_exempt
def ethTransfer(request):
    chainId = web3.eth.chain_id
    blockNum = web3.eth.block_number
    print("chainId :", chainId)
    print("blockNum :", blockNum)

    sync_status = web3.eth.syncing
    if sync_status:
        print("동기화 중입니다:", sync_status)
    else:
        print("동기화가 완료되었습니다.")
    try:
        userETHAddr = request.POST['userAddr']
        print("------------------------------모계좌 입금--------------------------------")
        Uaddr = userETHAddr
        print("userAddr :", Uaddr)
        Maddr = '0x1721DE2111C2061E9a67fB112728897E16705F04'
        UaddrCheckSumAddr = web3.to_checksum_address(Uaddr)
        MaddrCheckSumAddr = web3.to_checksum_address(Maddr)
        userAddr1 = web3.eth.get_balance(UaddrCheckSumAddr)
        print('userAddr0000000', userAddr1)
        userAddr = userAddr1 / 1000000000000000000
        print('userAddr: ',userAddr)
        if userAddr >= 0.05 and UaddrCheckSumAddr != "0xf7387cEbDCE62AFBc14A134924323B2337A9A94a":
          print('보내는 계좌: ', Uaddr)
          print('받는 계좌:   ', Maddr)
          print('userAddr: ', userAddr)
          valueAddr = userAddr1 - 2000000000000000
          print('1', valueAddr)
          getPrice = web3.eth.gas_price
          print('2', getPrice)
          totalGas = int(getPrice * 21000)
          print('3', totalGas)
        #   sendTx = web3.geth.personal.sendTransaction({
        #       "from": UaddrCheckSumAddr,
        #       "gasPrice": getPrice,
        #       "gas": "21000",
        #       "to": MaddrCheckSumAddr,
        #       "value": valueAddr,
        #       "data": ""
        #   }, 'asd123!')
          tx_hash = send_transaction(UaddrCheckSumAddr, MaddrCheckSumAddr, valueAddr, getPrice, 21000, 'asd123!')
          print(tx_hash)
          print('4')
          print('       |------------------(영수증)-------------------|')
          print('             보내는 계좌 잔액: ', web3.from_wei(userAddr, 'ether'))
          print('             보내는 금액:      ', web3.from_wei(valueAddr, 'ether'))
          print('                    ++++++++++++++++++++++')
          print('             가스비:           ', web3.from_wei(totalGas, 'ether'))
          print('       |---------------------------------------------|')
        else:
          print('ETH 0.05 미만 (그냥유지)')
        print("------------------------------------------------------------------------")

        # print("------------------------순수입금(print제외)---------------------------------")
        # fromAddr = "0x1905971093F2C80F8fD23C222201F643076Cf462"
        # toAddr = "0x7dF3FdE44988E4978B790181dBBbB11e2539497b"
        # fromCheckSumAddr = web3.to_checksum_address(fromAddr)
        # toCheckSumAddr = web3.to_checksum_address(toAddr)
        # getPrice = web3.eth.gasPrice;
        # addrEth = 0.01 * 1000000000000000000
        # addrEth = int(addrEth)
        # sendTx = web3.geth.personal.sendTransaction({
        #     "from": fromCheckSumAddr,
        #     "gasPrice": getPrice,
        #     "gas": "80000",
        #     "to": toCheckSumAddr,
        #     "value": addrEth,
        #     "data": ""
        # }, 'asd123!')
        # print("----------------------------------------------------------------------------")
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)
#
# def index(request):
#     context = {}
#     # template = loader.get_template('app/adminlogin.html')
#     return redirect('start')
#     # return HttpResponse(template.render(context, request))
# def start(request):
#     try:
#         return render(request, 'index.html')
#     except Exception as error:
#     	print("start", error)

@csrf_exempt
def checkEmail(request):
    try:
        email = request.POST.get('email')
        emailCheck = SignUp.objects.filter(email = email).count()
        if emailCheck > 0:
            print('email 있음 - 사용불가')
            context = {'value':'1'}
            return HttpResponse(json.dumps(context))
        elif emailCheck == 0:
            print("email 없음 - 사용가능")
            context = {'value':'0'}
            return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def checkUser(request):
    name = request.POST.get('RSLT_NAME')
    CI = request.POST.get('CI')
    DI = request.POST.get('DI')
    phone = request.POST.get('TEL_NO')
    signinfocount = SignUp.objects.filter(name=name,CI=CI,DI=DI,phone=phone).count()
    if signinfocount > 0:
        print("있음")
        userinfo = SignUp.objects.get(name=name,CI=CI,DI=DI,phone=phone)
        username = userinfo.username
        lastThree = username[len(username)-3:]
        replacename = username.replace(lastThree, "***")

        context = {"result":"1","msg":"본인인증에 성공했습니다.","replacename":username}
    elif signinfocount == 0:
        print("없음")
        context = {"result":"0","msg":"가입된 정보가 없습니다."}
    return HttpResponse(json.dumps(context))

@csrf_exempt
def signup(request):
    print("signup 호출됨")
    try:
        if request.method == "POST":
            form = signUpForm(request.POST)
            print("form", form)
            if form.is_valid():
                print("form 유효함")
                username = request.POST.get('username')
                
                username = request.POST['username']
                password = request.POST['password']
                otpCode = request.POST['otpCode']
                name = request.POST['name']
                phone = request.POST['phone']

                DI = request.POST.get('DI', '')
                CI = request.POST.get('CI', '')
                CP_CD = request.POST.get('CP_CD', '')
                TX_SEQ_NO = request.POST.get('TX_SEQ_NO', '')
                RSLT_CD = request.POST.get('RSLT_CD', '')
                TEL_COM_CD = request.POST.get('TEL_COM_CD', '')

                new_user = SignUp.objects.create_user(**form.cleaned_data)

                user = authenticate(username=username,password=password)
                if user:
                    userinfo = SignUp.objects.get(username=username)
                    userinfo.otpCode = otpCode
                    userinfo.name = name
                    userinfo.phone = phone
                    userinfo.email = username

                    userinfo.DI = DI
                    userinfo.CI = CI
                    userinfo.CP_CD = CP_CD
                    userinfo.TX_SEQ_NO = TX_SEQ_NO
                    userinfo.RSLT_CD = RSLT_CD
                    userinfo.TEL_COM_CD = TEL_COM_CD

                    userinfo.save()
                    context = {'value':'1'}
                    return HttpResponse(json.dumps(context))
                else:
                    context = {'value':'-9'}
                    return HttpResponse(json.dumps(context))
            else:
                print("form is not valid")
                print(form.errors)
                context = {'value': '-1', 'errors': form.errors}  # 에러 메시지를 응답에 포함
                return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def certify(request):
    print("certify 호출됨!")  # 서버에서 요청이 들어왔는지 확인
    try :
        context = {'value':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def login(request):
    print("Login view 호출됨!")  # 서버에서 요청이 들어왔는지 확인
    password = '115010'
    hashed_password = make_password(password)
    print(hashed_password)
    try:
        login_form = loginForms(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            usercount = SignUp.objects.filter(username = username).count()
            if usercount > 0:
                user = authenticate(username=username,password=password)
                print(user)
                if user:
                    auth_login(request, user)
                    useri = SignUp.objects.get(username=username);
                    print("----------------userLoginDateUp--------------------")
                    print(username," 님이 로그인을 하였습니다.")
                    print("----------------userLoginDateUp--------------------")
                    useri.date_joined = useri.date_joined.strftime('%Y-%m-%d %H:%M:%S')
                    useri.last_login = useri.last_login.strftime('%Y-%m-%d %H:%M:%S')
                    useri = model_to_dict(useri)

                    context = {'value':'1', 'user':useri}
                    return HttpResponse(json.dumps(context))
                else:
                    login_form.add_error(None, '비밀번호가 올바르지 않습니다.')
                    context = {'value':'-9'}
                    return HttpResponse(json.dumps(context))
            else:
                context = {'value':'2'}
                return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def userLoginDateUp(request):
	try:
		userID = request.POST.get('userID')
		userinfo = SignUp.objects.get(username = userID)
		userinfo.last_login = datetime.now()
		userinfo.save()

		useri = SignUp.objects.get(username = userID)
		useri.date_joined = useri.date_joined.strftime('%Y-%m-%d %H:%M:%S')
		useri.last_login = useri.last_login.strftime('%Y-%m-%d %H:%M:%S')

		context = {'value':'1', 'user':useri}
		username = userinfo.username
		print("----------------userLoginDateUp--------------------")
		print(username," 님이 자동 로그인으로 로그인을 하였습니다.")
		print("----------------userLoginDateUp--------------------")
		useri = model_to_dict(useri)



		context = {'result':'1', 'user':useri}
		return HttpResponse(json.dumps(context))
	except Exception as error:
		print(error)

@csrf_exempt
def checkOTPCode(request):
    try:
        userID = request.POST.get('userID')
        print("userID", userID)
        # userinfo = SignUp.objects.get(username = userID)
        userinfo = SignUp.objects.get(username = userID)
        otpCode = userinfo.otpCode

        context = {'result':'1', 'otpCode':otpCode}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)

# 비밀번호 재설정 시 otp 체크
@csrf_exempt
def checkOTPCode2(request):
    try:
        userID = request.POST.get('userID')
        print("userID", userID)
        userinfo = SignUp.objects.get(username = userID)

        otpCode = userinfo.otpCode
        context = {'result':'1', 'otpCode':otpCode}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)

@csrf_exempt
def userSettingModiPW(request):
    try:
        userID = request.POST.get('userID')
        pw = request.POST.get('pw')

        userinfo = SignUp.objects.get(username = userID)
        userinfo.set_password(pw)
        userinfo.save()

        context = {'result':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('userSettingModiPW', error)

@csrf_exempt
def updateUserinfo(request):
    try:
        userID = request.POST.get("userID")
        
        useri = SignUp.objects.get(id = userID)
        useri.date_joined = useri.date_joined.strftime('%Y-%m-%d %H:%M:%S')
        useri.last_login = useri.last_login.strftime('%Y-%m-%d %H:%M:%S')
        
        useri = model_to_dict(useri)
        context = {'value':'1', 'user':useri}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def web3newAcc(request):
    try:
        userID = request.POST.get('userID')
        pw = request.POST.get('pw')

        account = web3.eth.account.create('asd123!');
        print("account.address 의 값은? ", account.address)

        userinfo = SignUp.objects.get(id = userID)
        userinfo.ethAddr = account.address
        userinfo.save()

        print("----------------------------------------계좌생성 및 저장 완료----------------------------------------")

        context = {'value':'1'}
        return HttpResponse(json.dumps(context))

    except Exception as error:
        print(error)
        context = {'value':'-99'}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def newsinfo(request):
    try:
        print("뉴스를 DB를 출력함!!!")
        SafeNewsinfo = SafeNews.objects.all().order_by('-newsRegisDate')
        SafeNewsinfo = serializers.serialize('json', SafeNewsinfo)
        newCount0 = SafeNews.objects.filter(newsClass = 0, newsStatus = 0).count()
        newCount1 = SafeNews.objects.filter(newsClass = 1, newsStatus = 0).count()
        newCount2 = SafeNews.objects.filter(newsClass = 2, newsStatus = 0).count()
        appCount = newCount0 + newCount1 + newCount2
        print('newCount0: ', newCount0)
        print('newCount1: ', newCount1)
        print('newCount2: ', newCount2)
        print('appCount: ', appCount)

        context = {'result':'1', "SafeNewsinfo":SafeNewsinfo, "newCount0":newCount0, 'newCount1': newCount1, 'newCount2': newCount2, 'appCount': appCount }
        return HttpResponse(json.dumps(context))

    except Exception as error:
        print('newsinfo', error)

@csrf_exempt
def SolutionIng(request):
    try:
        userPK = request.POST.get('userID')
        print('솔루션대기 페이지 출력~!')
        SolutionIngInfo = SolutionList.objects.filter(soluStatus=0).order_by('-soluRegisDate')
        SolutionIngInfo = serializers.serialize('json', SolutionIngInfo)
        SolutionIngInfo2 = SolutionList.objects.filter(userPK=userPK , soluStatus=0).count()
        print(SolutionIngInfo)

        context = {'value':'777', "SolutionIngInfo":SolutionIngInfo, "SolutionIngInfo2":SolutionIngInfo2}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("SolutionRequest", error)

@csrf_exempt
def MySolution(request):
    try:
        print('내 솔루션 페이지 출력~!')
        userPK = request.POST.get('userID')
        mySolutionInfo = SolutionList.objects.filter(soluStatus=1).order_by('-soluRegisDate')
        mySolutionInfo = serializers.serialize('json', mySolutionInfo)
        mySolutionInfo2 = SolutionList.objects.filter(userPK=userPK , soluStatus=1).count()
        print(mySolutionInfo)
        print(mySolutionInfo2)

        context = {'value':'777', "mySolutionInfo":mySolutionInfo, "mySolutionInfo2":mySolutionInfo2}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("SolutionRequest", error)

@csrf_exempt
def SolutionRequest(request):
    try:
        print("SolutionRequest가 실행됨!")
        userPK = request.POST.get('userID')
        userEmail = request.POST.get('userEmail')
        userName = request.POST.get('userName')
        userPhone = request.POST.get('userPhone')
        buildingType = request.POST.get('buildingType')
        SoluImg1 = request.POST.get('solutionImg1')
        SoluImg2 = request.POST.get('solutionImg2')
        SoluImg3 = request.POST.get('solutionImg3')
        SoluImg4 = request.POST.get('solutionImg4')
        SoluImg5 = request.POST.get('solutionImg5')
        SoluImg6 = request.POST.get('solutionImg6')
        today = datetime.now()
        y = str(today.year)
        m = str(today.month)
        d = str(today.day)
        day = str(y+'/'+m+'/'+d)
        solutionImgList = request.POST.get('solutionImgList')
        solutionImgList = solutionImgList.split(',')
        print("solutionImgList >>>>", solutionImgList)
        print("solutionImgList >>>>", type(solutionImgList))

        solutionImgListDay = []
        for i in solutionImgList:
            print(i)
            solutionImgListDay.append(day+"/"+i)

        print("solutionImgListDay >>>>", solutionImgListDay)
        solutionImgListDay = ','.join(solutionImgListDay)
        print("solutionImgListDay >>>>", solutionImgListDay)

        print("userPK의 값은? ", userPK)
        print("userEmail 값은? ", userEmail)
        print("userName 값은? ", userName)
        print("userPhone 값은? ", userPhone)
        print("buildingType 값은? ", buildingType)
        print("SoluImg1 값은? ", SoluImg1)

        SolutionListinfo = SolutionList.objects.create()
        SolutionListinfo.soluRegisDate = datetime.now()

        # if buildingType == "0":
        #     SolutionListinfo.buildingType = "아파트"
        # elif buildingType == "1":
        #     SolutionListinfo.buildingType = "빌라"
        # elif buildingType == "2":
        #     SolutionListinfo.buildingType = "오피스텔"
        # elif buildingType == "3":
        #     SolutionListinfo.buildingType = "전원주택"
        # elif buildingType == "4":
        #     SolutionListinfo.buildingType = "상가주택"
        # elif buildingType == "5":
        #     SolutionListinfo.buildingType = "한옥주택"
        # elif buildingType == "6":
        #     SolutionListinfo.buildingType = "원룸"
        # elif buildingType == "7":
        #     SolutionListinfo.buildingType = "투룸"
        # elif buildingType == "8":
        #     SolutionListinfo.buildingType = "사무실"
        # elif buildingType == "9":
        #     SolutionListinfo.buildingType = "상가"
        # else:
        #     SolutionListinfo.buildingType = "(기타) "+buildingType

        if buildingType == "0":
            SolutionListinfo.buildingType = "빌딩"
        elif buildingType == "1":
            SolutionListinfo.buildingType = "아파트"
        elif buildingType == "2":
            SolutionListinfo.buildingType = "오피스텔"
        elif buildingType == "3":
            SolutionListinfo.buildingType = "상가"
        elif buildingType == "4":
            SolutionListinfo.buildingType = "사무실"
        elif buildingType == "5":
            SolutionListinfo.buildingType = "다세대빌라"
        elif buildingType == "6":
            SolutionListinfo.buildingType = "단독주택"
        # elif buildingType == "7":
        #     SolutionListinfo.buildingType = "투룸"
        # elif buildingType == "8":
        #     SolutionListinfo.buildingType = "사무실"
        # elif buildingType == "9":
        #     SolutionListinfo.buildingType = "상가"
        # else:
        #     SolutionListinfo.buildingType = "(기타) "+buildingType

        SolutionListinfo.paidGDST = "50"
        SolutionListinfo.userEmail = userEmail
        SolutionListinfo.userName = userName
        SolutionListinfo.userphone = userPhone
        SolutionListinfo.soluStatus = "0"
        SolutionListinfo.userPK = userPK
        SolutionListinfo.SoluImg1 = solutionImgListDay
        SolutionListinfo.SoluImg2 = None
        SolutionListinfo.SoluImg3 = None
        SolutionListinfo.SoluImg4 = None
        SolutionListinfo.SoluImg5 = None
        SolutionListinfo.SoluImg6 = None
        SolutionListinfo.save()

        userinfo = SignUp.objects.get(id = userPK)
        userinfo.tempSoluImg1 = None
        userinfo.tempSoluImg2 = None
        userinfo.tempSoluImg3 = None
        userinfo.tempSoluImg4 = None
        userinfo.tempSoluImg5 = None
        userinfo.tempSoluImg6 = None
        userinfo.save()
        context = {'value':'777'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
      print("SolutionRequest", error)

@csrf_exempt
def solution1Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                print('changeImg>>>>>>>>>>>>>>>>>>>>', changeImg)
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg1 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution1UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg1 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solution2Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg2 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution2UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg2 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solution3Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg3 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution3UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg3 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solution4Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg4 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution4UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg4 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solution5Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg5 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution5UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg5 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solution6Upload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)
                userinfo = SignUp.objects.get(id = userID)
                userinfo.tempSoluImg6 = str(y+'/'+m+'/'+d+'/'+str(changeImg))
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))

@csrf_exempt
def solution6UpImgDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.tempSoluImg6 = None
        userinfo.ImgCount -= 1
        userinfo.save()
        context = {'result':'1', 'userinfo': userinfo.ImgCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def solutionPageDel(request):
    try:
        userID = request.POST.get('userID')
        userinfo = SignUp.objects.get(id = userID)
        userinfo.ImgCount = 0
        userinfo.tempSoluImg1= None
        userinfo.tempSoluImg2= None
        userinfo.tempSoluImg3= None
        userinfo.tempSoluImg4= None
        userinfo.tempSoluImg5= None
        userinfo.tempSoluImg6= None
        userinfo.save()
        context = {'result':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def TESDGDS(request):
    try:
        print("----------------------------토큰 출금------------------------------")
        # -----------------------------------------------------------------------------
        fromAddr = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'
        toAddr = '0x49b4C5481d33ab4A3ddDb9bF68be0574A4fe02C6'
        # -----------------------------------------------------------------------------
        fromAddrChecksum = web3.to_checksum_address(fromAddr)
        toAddrChecksum = web3.to_checksum_address(toAddr)
        print('       |-----------------(영수증)--------------------|')
        TokenC_I = tokenContract(address=web3.to_checksum_address("0x34bfb68cca8d174192f0e1a63ba3fdf50741ac4e"))
        unRock = web3.geth.personal.unlockAccount(fromAddrChecksum, "asd123!", 10)
        print('          ---------------토큰 집금----------------')
        print('                        unRock: ', unRock)
        test = TokenC_I.functions.transfer(toAddrChecksum, web3.toWei(1000,"ether")).transact({'gas' : 5000, "from": fromAddrChecksum})
        print('                        토큰 전송 중...')
        print('                        토큰 전송 완료')
        rock = web3.geth.personal.lockAccount(fromAddrChecksum)
        print('                        Rock:   ', rock)
        print('Txn Hash: ',test.hex())
        print('       |---------------------------------------------|')
        context = {'result':'1'}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('1', error)

@csrf_exempt
def gdsclookTime(request):
    try:
        timeBtn = request.POST.get('timeBtn')
        userPK = request.POST.get('userPK')
        userA = request.POST.get('userA')
        gdstWall = request.POST.get('gdstWall')
        if timeBtn == '' :
          timeStart = request.POST.get('timeStart')
          timeEnd = request.POST.get('timeEnd')
          print(timeStart, ' - ', timeEnd)
          if gdstWall == 'in':
            print('in')
            timeValue = UsergdscWallet.objects.filter(datetime__range = [timeStart, timeEnd], tokenName = 'abcd', to = userA.lower()).order_by('-datetime')
            timeValueCount = UsergdscWallet.objects.filter(datetime__range = [timeStart, timeEnd], tokenName = 'abcd', to = userA.lower()).count()
            timeValue = serializers.serialize('json', timeValue)
          elif gdstWall == 'out':
            print('out')
            timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [timeStart, timeEnd], tokenName = 'abcd', fromAddr = userA).order_by('-datetime')
            timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'),datetime__range = [timeStart, timeEnd], tokenName = 'abcd', fromAddr = userA).count()
            timeValue = serializers.serialize('json', timeValue)
          elif gdstWall == 'all':
            print('all')
            timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [timeStart, timeEnd], tokenName = 'abcd').order_by('-datetime')
            timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [timeStart, timeEnd], tokenName = 'abcd').count()
            timeValue = serializers.serialize('json', timeValue)
          print('timeValueCount: ', timeValueCount)
        else :
          if timeBtn == '오늘':
            print('오늘')
            now1 = datetime.now()
            now1 = now1 - timedelta(days=1)
            now2 = now1 + timedelta(days=2)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now1 , ' - ', now2)
            if gdstWall == 'in':
              print('in')
              timeValue = UsergdscWallet.objects.filter(datetime__range = [now1, now2], tokenName = 'abcd', to = userA.lower()).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(datetime__range = [now1, now2], tokenName = 'abcd', to = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now1, now2], tokenName = 'abcd', fromAddr = userA).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'),datetime__range = [now1, now2], tokenName = 'abcd', fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now1, now2], tokenName = 'abcd').order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now1, now2], tokenName = 'abcd').count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
          elif timeBtn == '1개월':
            print('1개월')
            now1 = datetime.now()
            now1 = now1 + timedelta(days=1)
            now2 = now1 - timedelta(days=30)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now2, ' ~ ', now1)
            if gdstWall == 'in':
              print('in')
              timeValue = UsergdscWallet.objects.filter(datetime__range = [now2, now1], tokenName = 'abcd', to = userA.lower()).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(datetime__range = [now2, now1], tokenName = 'abcd', to = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd', fromAddr = userA).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'),datetime__range = [now2, now1], tokenName = 'abcd', fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd').order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd').count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
          elif timeBtn == '3개월':
            print('3개월')
            now1 = datetime.now()
            now1 = now1 + timedelta(days=1)
            now2 = now1 - timedelta(days=90)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now2, ' ~ ', now1)
            if gdstWall == 'in':
              print('in')
              timeValue = UsergdscWallet.objects.filter(datetime__range = [now2, now1], tokenName = 'abcd', to = userA.lower()).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(datetime__range = [now2, now1], tokenName = 'abcd', to = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd', fromAddr = userA).order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'),datetime__range = [now2, now1], tokenName = 'abcd', fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd').order_by('-datetime')
              timeValueCount = UsergdscWallet.objects.filter(~Q(to = '0xf30e4E3B851Fc505596Fd603b43cB2Bfcc6132C6'), datetime__range = [now2, now1], tokenName = 'abcd').count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
        context = {'result':'1', 'timeValue': timeValue, 'timeValueCount': timeValueCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)

@csrf_exempt
def ethlookTime(request):
    try:
        timeBtn = request.POST.get('timeBtn')
        userPK = request.POST.get('userPK')
        userA = request.POST.get('userA')
        print("------------------userA :", userA)
        gdstWall = request.POST.get('gdstWall')
        if timeBtn == '' :
          timeStart = request.POST.get('timeStart')
          timeEnd = request.POST.get('timeEnd')
          print(timeStart, ' - ', timeEnd) #기간 설정에서 직접입력
          if gdstWall == 'in':
            print('in') #입금은 수수료 d
            timeValue = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [timeStart, timeEnd], gasUsed = 21000, toAddr = userA.lower()).order_by('-timeStamp') #to는 ether스캔 api로 오는데 소문자로 옴
            timeValueCount = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [timeStart, timeEnd], gasUsed = 21000, toAddr = userA.lower()).count()
            timeValue = serializers.serialize('json', timeValue)
          elif gdstWall == 'out':
            print('out') #출금은 Maddr d
            timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [timeStart, timeEnd], gasUsed = 21000, fromAddr = userA).order_by('-timeStamp') #from은 데이터베이스에 대소문자 구분되서 저장 됨
            timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [timeStart, timeEnd], gasUsed = 21000, fromAddr = userA).count()
            timeValue = serializers.serialize('json', timeValue)
          elif gdstWall == 'all':
            print('all')
            timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [timeStart, timeEnd], gasUsed = 21000).order_by('-timeStamp')
            timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [timeStart, timeEnd], gasUsed = 21000).count()
            timeValue = serializers.serialize('json', timeValue)
          print('timeValueCount: ', timeValueCount)
        else :
          if timeBtn == '오늘':
            print('오늘')
            now1 = datetime.now()
            now1 = now1 - timedelta(days=1)
            now2 = now1 + timedelta(days=2)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now1 , ' - ', now2)
            if gdstWall == 'in':
              print('in')
              timeValue = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now1, now2], gasUsed = 21000, toAddr = userA.lower()).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now1, now2], gasUsed = 21000, toAddr = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now1, now2], gasUsed = 21000, fromAddr = userA).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now1, now2], gasUsed = 21000, fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now1, now2], gasUsed = 21000).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now1, now2], gasUsed = 21000).count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
          elif timeBtn == '1개월':
            print('1개월')
            now1 = datetime.now()
            now1 = now1 + timedelta(days=1)
            now2 = now1 - timedelta(days=30)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now2, ' ~ ', now1)
            if gdstWall == 'in':
              print('in')
              timeValue = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, toAddr = userA.lower()).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, toAddr = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000, fromAddr = userA).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000).count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
          elif timeBtn == '3개월':
            print('3개월')
            now1 = datetime.now()
            now1 = now1 + timedelta(days=1)
            now2 = now1 - timedelta(days=90)
            now1 = now1.strftime('%Y-%m-%d')
            now2 = now2.strftime('%Y-%m-%d')
            print(now2, ' ~ ', now1)
            if gdstWall == 'in':
              print('in')
              timeValue = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, toAddr = userA.lower()).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(fromAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, toAddr = userA.lower()).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'out':
              print('out')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000, fromAddr = userA).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'),timeStamp__range = [now2, now1], gasUsed = 21000, fromAddr = userA).count()
              timeValue = serializers.serialize('json', timeValue)
            elif gdstWall == 'all':
              print('all')
              timeValue = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000).order_by('-timeStamp')
              timeValueCount = UserEthWallet.objects.filter(~Q(toAddr = '0xf7387cEbDCE62AFBc14A134924323B2337A9A94a'), timeStamp__range = [now2, now1], gasUsed = 21000).count()
              timeValue = serializers.serialize('json', timeValue)
            print('timeValueCount: ', timeValueCount)
        context = {'result':'1', 'timeValue': timeValue, 'timeValueCount': timeValueCount}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print('myProfileDel', error)


# -------------------------------------------------------------------------------------------------------------------------------------------------------
# 2022.07.19 - JS / 솔루션 이미지등록 수정

@csrf_exempt
def solutionUpload(request):
    try:
        if request.method == 'POST':
            doc = request.FILES #returns a dict-like object
            if len(request.FILES['file']) != 0:
                changeImg = request.FILES['file']
                print('changeImg>>>>>>>>>>>>>>>>>>>>', changeImg)
                splidata = str(changeImg).split('.')
                userID = request.POST.get('value1')
                today = datetime.now()
                y = str(today.year)
                m = str(today.month)
                d = str(today.day)
                day = str(y+'/'+m+'/'+d)
                # path = '/mnt/project/app/static/auctionImg/'+userID+/'+y+'/'+m+'/'+d+'/'
                path = '/mnt/GDSC/app/static/solutionImg/'+userID+'/'+day+'/'
                if not os.path.exists(path):
                    os.makedirs(path)
                if os.path.isfile(path +str(changeImg)):
                    os.remove(path +str(changeImg))
                with open(path +str(changeImg), 'wb+') as destination:
                    for chunk in changeImg.chunks():
                        destination.write(chunk)

                userinfo = SignUp.objects.get(id = userID)
                userinfo.ImgCount += 1
                userinfo.save()
        context = {"value":"1", 'day':day}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))



@csrf_exempt
def smsTest(request):
    try:
        account_sid = os.getenv("ACCOUNT_SID")
        auth_token  = os.getenv("AUTH_TOKEN")
        client = Client(account_sid, auth_token)

         # 걸러진 전화번호를 저장하여 message API 사용
        # message = client.messages.create(to='+821022239856',from_="+821022239856",body="<메세지 내용>")
        message = client.messages.create(body="<메세지 내용>",from_="+19475002669",to='+821022239856')
        context = {"value":"1"}
        return HttpResponse(json.dumps(context))
    except Exception as error:
        print("artiAuction1Upload : ", error)
        context = {"value":"-99"}
        return HttpResponse(json.dumps(context))
