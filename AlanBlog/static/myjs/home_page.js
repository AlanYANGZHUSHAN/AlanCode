var starturl = "";

var apiurl = {
    getContentListUrl : '/homepage/content/get',
    addOneItemUrl: '/homepage/content/add',
    addOneFileUrl: '/homepage/content/addfile',
    picToEpsUrl: '/homepage/content/pictoeps'
};

$(document).ready(function(){
    vue["homePage"].init();
});

var vue = {
    homePage : new Vue ({
        delimiters : ['<%', '%>'],
        mounted : function() {
        },
        el: '#home_page',
        data:{
            content_list:[],
            start_date:'',
            end_date: '',
            tag:'--select tag--',
            author:'',
            title: '',
            isShowAddDetail: false,
            uploadfile:null,
            isShowPicTran: false,
        },
        methods : {
            init: function() {
                var _homepageThis = this;
                var now_date = (new Date()).valueOf();
                var now_date_array = this.$options.methods.formatDate.bind(this)(now_date);
                var start_date = now_date - 24*60*60*1000;
                var start_date_array =  this.$options.methods.formatDate.bind(this)(start_date);
                _homepageThis.start_date = start_date_array[1];
                _homepageThis.end_date = now_date_array[1];
                this.$options.methods.queryData.bind(this)();
                _homepageThis.isShowPicTran = false;
                _homepageThis.isShowAddDetail = false;
            },
            formatDate: function(time_params){
                var now_time = new Date(time_params);
                var now_time_stamp = Math.round(now_time/1000);
                var time = ((now_time.toLocaleString()).split(' ')[0]).split('/');
                var year = time[0];
                var month = time[1];
                var day = time[2];

                if(month.length == 1){
                    month = '0' + month;
                };

                if(day.length == 1){
                    day = '0' + day;
                };
                var now_time_format = year + '-' + month + '-' + day;
                return [now_time_stamp, now_time_format];
            },

            queryData: function(){
                var _queryDataThis = this;
                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    url :  starturl + apiurl.getContentListUrl,
                    data: JSON.stringify({start_date:_queryDataThis.start_date, end_date:_queryDataThis.end_date, tag:_queryDataThis.tag}),
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            var result = response['result'];
                            _queryDataThis.content_list = result;
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert('msg');
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

            },
            subPage: function(item){
                window.open('../../static/myhtml/'+item.url,'_blank','width=600,height=400,top=100px,left=0px,toolbar=yes,scrollbars=yes,status=yes,menubar=yes')
            },
            showAddDetail: function(){
                this.isShowAddDetail = true;
            },
            closeAddDetail: function(){
                this.isShowAddDetail = false;
            },

            addData: function(){
                var _addDataThis = this;
                this.$options.methods.submitFile.bind(this)();

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.addOneItemUrl,
                    data: JSON.stringify({title:_addDataThis.title, tag:_addDataThis.tag, author:_addDataThis.author, url: _addDataThis.url}),
                    processData: false, 
                    contentType: false, 
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            alert('操作成功');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });

           
            },
            submitFile : function(){
                var form = new FormData();
                form.append("file", this.uploadfile);

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.addOneFileUrl,
                    data: form,
                    contentType: false,  
                    processData: false,  
                    success:function(response){
                        var status = response['status'];
                        if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }

                });
            },
            onfilechange : function(e){
                var files = e.target.files || e.dataTransfer.files;
                if (!files.length){
                    return;
                };
                this.uploadfile = files[0];
                this.url = files[0].name;
            },
            picTran : function(){
                var _picTranThis = this;
                this.$options.methods.submitFile.bind(this)();

                $.ajax({
                    type : 'post',
                    dataType : 'json',
                    async : false,
                    url: starturl + apiurl.picToEpsUrl,
                    data: JSON.stringify({From_fileName:this.url}),
                    processData: false, 
                    contentType: false, 
                    success:function(response){
                        var status = response['status'];
                        if(status == 'SUCCESS'){
                            $('#pic_tran').attr('href','../static/myhtml/'+response['To_fileName']);
                            $('#pic_tran').attr('download',response['To_fileName']);
                            $('#pic_tran').text('点击下载');
                            alert('操作成功');
                        }else if(status == 'FAIL'){
                            var msg = response['msg'];
                            alert(msg);
                        };
                    },
                    error:function(response){
                        alert('请求出错');
                    }
                })
            },
            showPicTran : function(){
                this.isShowPicTran = true;
            },
            closePicTran : function(){
                this.isShowPicTran = false;
            }


        }


    })

};

