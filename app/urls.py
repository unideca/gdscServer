# from django.urls import path, re_path
from django.urls import re_path  # re_path는 django.urls에서 가져와야 합니다.
from django.conf.urls import handler400, handler403, handler404, handler500  # handler들은 django.conf.urls에서 가져옵니다.
from app import views , web3Views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^certify/$', views.certify, name='certify'),
    re_path(r'^newAccount/$', views.newAccount, name='newAccount'),
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^checkEmail/$', views.checkEmail, name='checkEmail'),
    re_path(r'^checkUser/$', views.checkUser, name='checkUser'),
    re_path(r'^checkOTPCode/$', views.checkOTPCode, name='checkOTPCode'),
    re_path(r'^checkOTPCode2/$', views.checkOTPCode2, name='checkOTPCode2'),
    re_path(r'^userSettingModiPW/$', views.userSettingModiPW, name='userSettingModiPW'),
    re_path(r'^userLoginDateUp/$', views.userLoginDateUp, name='userLoginDateUp'),
    re_path(r'^updateUserinfo/$', views.updateUserinfo, name='updateUserinfo'),
    re_path(r'^web3newAcc/$', views.web3newAcc, name='web3newAcc'),
    re_path(r'^newsinfo/$', views.newsinfo, name='newsinfo'),

    re_path(r'^SolutionRequest/$', views.SolutionRequest, name='SolutionRequest'),
    re_path(r'^SolutionIng/$', views.SolutionIng, name='SolutionIng'),
    re_path(r'^MySolution/$', views.MySolution, name='MySolution'),
    re_path(r'^solution1Upload/$', views.solution1Upload, name='solution1Upload'),
    re_path(r'^solution1UpImgDel/$', views.solution1UpImgDel, name='solution1UpImgDel'),
    re_path(r'^solution2Upload/$', views.solution2Upload, name='solution2Upload'),
    re_path(r'^solution2UpImgDel/$', views.solution2UpImgDel, name='solution2UpImgDel'),
    re_path(r'^solution3Upload/$', views.solution3Upload, name='solution3Upload'),
    re_path(r'^solution3UpImgDel/$', views.solution3UpImgDel, name='solution3UpImgDel'),
    re_path(r'^solution4Upload/$', views.solution4Upload, name='solution4Upload'),
    re_path(r'^solution4UpImgDel/$', views.solution4UpImgDel, name='solution4UpImgDel'),
    re_path(r'^solution5Upload/$', views.solution5Upload, name='solution5Upload'),
    re_path(r'^solution5UpImgDel/$', views.solution5UpImgDel, name='solution5UpImgDel'),
    re_path(r'^solution6Upload/$', views.solution6Upload, name='solution6Upload'),
    re_path(r'^solution6UpImgDel/$', views.solution6UpImgDel, name='solution6UpImgDel'),
    re_path(r'^userSendGDSC/$', views.userSendGDSC, name='userSendGDSC'),
    re_path(r'^ethTransfer/$', views.ethTransfer, name='ethTransfer'),
    re_path(r'^allAmount/$', views.allAmount, name='allAmount'),
    re_path(r'^ethWithdraw/$', views.ethWithdraw, name='ethWithdraw'),
    re_path(r'^TtoClist/$', views.TtoClist, name='TtoClist'),
    re_path(r'^userEthWallet111/$', views.userEthWallet111, name='userEthWallet111'),
    re_path(r'^userEthWalletSave/$', views.userEthWalletSave, name='userEthWalletSave'),
    re_path(r'^userEthWalletList/$', views.userEthWalletList, name='userEthWalletList'),
    re_path(r'^addrcheck/$', views.addrcheck, name='addrcheck'),
    re_path(r'^TtoCsave/$', views.TtoCsave, name='TtoCsave'),
    re_path(r'^CtoTsave/$', views.CtoTsave, name='CtoTsave'),
    re_path(r'^userGDSCWalletSave/$', views.userGDSCWalletSave, name='userGDSCWalletSave'),
    re_path(r'^userGdscWalletList/$', views.userGdscWalletList, name='userGdscWalletList'),
    re_path(r'^gdscWithdraw/$', views.gdscWithdraw, name='gdscWithdraw'),
    re_path(r'^solutionPageDel/$', views.solutionPageDel, name='solutionPageDel'),
    re_path(r'^ethlookTime/$', views.ethlookTime, name='ethlookTime'),
    re_path(r'^TESDGDS/$', views.TESDGDS, name='TESDGDS'),
    re_path(r'^gdsclookTime/$', views.gdsclookTime, name='gdsclookTime'),
    re_path(r'^safenotifi/$', views.safenotifi, name='safenotifi'),
    re_path(r'^solutionnotifi/$', views.solutionnotifi, name='solutionnotifi'),
    re_path(r'^tokensava/$', views.tokensava, name='tokensava'),
    re_path(r'^bellset/$', views.bellset, name='bellset'),
    re_path(r'^bellsave/$', views.bellsave, name='bellsave'),



    # re_path(r'^testWall/$', web3Views.testWall, name='testWall'),
    # re_path(r'^testWall111/$', web3Views.testWall111, name='testWall111'),
    # re_path(r'^test4028/$', web3Views.test4028, name='test4028'),
    # re_path(r'^sendEthToUser/$', web3Views.sendEthToUser, name='sendEthToUser'),
    # re_path(r'^testtest/$', web3Views.testtest, name='testtest'),


    # --------------------------------------------------------------------------------
    # 2022.07.19 - JS / 솔루션 이미지등록 수정
    re_path(r'^solutionUpload/$', views.solutionUpload, name='solutionUpload'),
    # 2022.07.21 JS - SMS 테스트
    re_path(r'^smsTest/$', views.smsTest, name='smsTest'),




    # re_path(r'^solutionPageDel/$', views.solutionPageDel, name='solutionPageDel'),
]
# + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

    # re_path(r'^.*\.html', views.gentella_html, name='gentella'),
    # re_path(r'^', views.index, name='index'),
    # re_path('start', views.start, name='start'),
    # re_path(r'^start/$', views.start, name='start'),

    # path('signup', views.signup, name='signup'),
    # path('login', views.login, name='login'),
    # path('checkEmail', views.checkEmail, name='checkEmail'),
    # path('checkUser', views.checkUser, name='checkUser'),
    # path('checkOTPCode', views.checkOTPCode, name='checkOTPCode'),
    # path('checkOTPCode2', views.checkOTPCode2, name='checkOTPCode2'),
    # path('userSettingModiPW', views.userSettingModiPW, name='userSettingModiPW'),
    # path('userLoginDateUp', views.userLoginDateUp, name='userLoginDateUp'),
    # path('updateUserinfo', views.updateUserinfo, name='updateUserinfo'),
    # path('web3newAcc', views.web3newAcc, name='web3newAcc'),
    # path('newsinfo', views.newsinfo, name='newsinfo'),
    # path('newAccount', views.newAccount, name='newAccount'),
    # # path('newAccount', web3Views.newAccount, name='newAccount'),

    # path('SolutionRequest', views.SolutionRequest, name='SolutionRequest'),
    # path('SolutionIng', views.SolutionIng, name='SolutionIng'),
    # path('MySolution', views.MySolution, name='MySolution'),
    # path('solution1Upload', views.solution1Upload, name='solution1Upload'),
    # path('solution1UpImgDel', views.solution1UpImgDel, name='solution1UpImgDel'),
    # path('solution2Upload', views.solution2Upload, name='solution2Upload'),
    # path('solution2UpImgDel', views.solution2UpImgDel, name='solution2UpImgDel'),
    # path('solution3Upload', views.solution3Upload, name='solution3Upload'),
    # path('solution3UpImgDel', views.solution3UpImgDel, name='solution3UpImgDel'),
    # path('solution4Upload', views.solution4Upload, name='solution4Upload'),
    # # path('solution4UpImgDel', views.solution4UpImgDel, name='solution4UpImgDel'),
    # path('solution5Upload', views.solution5Upload, name='solution5Upload'),
    # path('solution5UpImgDel', views.solution5UpImgDel, name='solution5UpImgDel'),
    # path('solution6Upload', views.solution6Upload, name='solution6Upload'),
    # path('solution6UpImgDel', views.solution6UpImgDel, name='solution6UpImgDel'),
    # path('updateUserinfo', views.updateUserinfo, name='updateUserinfo'),
    # path('solutionPageDel', views.solutionPageDel, name='solutionPageDel'),
