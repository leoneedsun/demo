function News() {

}

News.prototype.initUEditor = function () {
    window.ue = UE.getEditor('editor', {
        'initialFrameHeight': 600,
        'serverUrl': '/ueditor/upload/'
    })
}

News.prototype.listenUploadFileEvent = function () {
    var uploadBtn = $('#thumbnail-btn')
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0]
        var formData = new FormData()
        formData.append('file', file)
        xfzajax.post({
            'url': '/cms/upload_file/',
            'data': formData,
            'processData': false,
            'contentType': false,
            'success': function (result) {
                if (result['code'] === 200) {
                    var url = result['data']['url']
                    var thumbnailInput = $('#thumbnail-form')
                    thumbnailInput.val(url)
                }
            }
        })
    })
}

News.prototype.listenQiniuUploadFileEvent = function () {
    var self = this
    var uploadBtn = $('#thumbnail-btn')
    uploadBtn.change(function () {
        var file = this.files[0]
        xfzajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                if (result['code'] === 200) {
                    var token = result['data']['token']
                    // 时间戳 与 x.jpg(将文件名通过'.'拆分开）即[x,jpg]的后者结合
                    // e.g. 20200627+.+jpg=20200627.jpg
                    // 问题：如果文件名为a.b.jpg，则拆分出的是b，所以需要进行遍历处理，如何处理？
                    var key = (new Date()).getTime() + '.' + file.name.split('.')[1]
                    var putExtra = {
                        fname: key,
                        params: {},
                        mimeType: ['image/png', 'image/jpeg', 'image/gif', 'video/x-ms-wmv']
                    }
                    var config = {
                        useCdnDomain: true,
                        retryCount: 6,
                        region: qiniu.region.z2
                    }
                    var observable = qiniu.upload(file, key, token, putExtra, config)
                    observable.subscribe({
                        'next': self.handleFileUploadProgress,
                        'error': self.handleFileUploadError,
                        'complete': self.handleFileUploadComplete
                    })
                }
            }
        })
    })
}

News.prototype.handleFileUploadProgress = function (response) {
    var total = response.total
    var percent = total.percent
    var percentText = percent.toFixed(0) + '%'
    var progressGroup = News.progressGroup
    progressGroup.show()
    var progressBar = $('.progress-bar')
    progressBar.css({'width': percentText})
    progressBar.text(percentText)
}

News.prototype.handleFileUploadError = function (error) {
    window.messageBox.showError(error.message)
    var progressGroup = $('#progress-group')
    progressGroup.hide()
    console.log(error.message)
}

News.prototype.handleFileUploadComplete = function (response) {
    console.log(response)
    var progressGroup = $('#progress-group')
    progressGroup.hide()

    var domain = 'qcqbm6k03.bkt.clouddn.com/'
    var filename = response.key
    var url = domain + filename
    var thumbnailInput = $("input[name='thumbnail']")
    thumbnailInput.val(url)
}

News.prototype.listenSubmitEvent = function () {
    var submint = $('#submit-btn')
    submint.click(function (event) {
        // preventDefault组织默认行为，因为是富文本编辑器，需要在点击提交按钮时组织默认的提交表单行为，通过JS获取内容再通过ajax发送给数据库
        event.preventDefault()
        var title = $("input[name='title']").val()
        var category = $("select[name='category']").val()
        var desc = $("input[name='desc']").val()
        var thumbnail = $("input[name='thumbnail']").val()
        var content = window.ue.getContent()

        xfzajax.post({
            'url': '/cms/write_news/',
            'data': {
                'title': title,
                'category': category,
                'desc': desc,
                'thumbnail': thumbnail,
                'content': content
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess('恭喜！新闻发表成功！', function () {
                        window.location.reload()
                    })
                }
            }
        })
    })
}

News.prototype.run = function () {
    var self = this
    // self.listenUploadFileEvent()
    self.listenQiniuUploadFileEvent()
    self.initUEditor()
    self.listenSubmitEvent()
}


$(function () {
    var news = new News()
    news.run()
    News.progressGroup = $('#progress-group')
})