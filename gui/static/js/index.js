new Vue({
    el: '#app',
    delimiters: ["[[", "]]"], 
    data() {
        return {
            testlist: [
                {
                    tab_name: "first",
                    name: "first",
                },
                {
                    tab_name: "2",
                    name: "2",
                },
                {
                    tab_name: "3",
                    name: "3",
                }
            ],
            fileList: {},
            panel_msg: "",
            play_sound_enabled: false,
            visualization_detection_enabled: false,
            source_liveRoom_enabled: false,
            source_liveRoom_url: '',
            source_record_enabled: false,
            source_record_device: '',
            attribute_name: "",
            attribute_gender: "",
            attribute_age: "",
            attribute_birth: "",
            attribute_zodiac: "",
            attribute_constellation: "",
            attribute_job: "",
            attribute_hobby: "",
            attribute_contact: "",
            attribute_voice: "",
            interact_perception_gift: 0,
            interact_perception_follow: 0,
            interact_perception_join: 0,
            interact_perception_chat: 0,
            interact_perception_indifferent: 0,
            interact_maxInteractTime: 15,
            interact_QnA: "",
            items_data: [],
            live_state: 0,
            device_list: [],
            send_msg:"",
            picture_url:"",
            // 用户信息
            user_inform:{
                name: "",
                gender: "",
                age: "",
                type:"",
                location:"",
                coordinate:"",
                sit_time:"",
                lay_time:"",
                med_inform:{
                    name:"",
                    spec:"",
                    usage:"",
                    freq:"",
                    dosage:"",
                    time:"",
                }
            },
            // device_list: [
            //     {
            //         value: '选项1',
            //         label: '麦克风'
            //     }
            // ],
            voice_list: [],
            options: [{
                value: '选项1',
                label: '黄金糕'
            }, {
                value: '选项2',
                label: '双皮奶'
            }],
            activeName: 'first',

            editableTabsValue: '1',
            tabIndex: 1,
            editableTabs: [{
                title: 'Tab 1',
                name: '1',
                content: 'Tab 1 content'
            }, {
                title: 'Tab 2',
                name: '2',
                content: 'Tab 2 content'
            }],
            msg_list:[]

        }
    },
    created() {
        window.addEventListener('keydown', this.handkeyCode, true)//开启监听键盘按下事件
    },
    methods: {
         // 回车和空格键提交右侧信息
        handkeyCode(e) {
        if(e.keyCode === 13 || e.keyCode === 18){
            this.send(2)
        }
        },
        handleTabsEdit(targetName, action) {
            if (action === 'add') {
                let newTabName = ++this.tabIndex + '';
                this.items_data.push({
                    tab_name: newTabName,
                    enabled: false,
                    name: "",
                    explain: {
                        intro: "",
                        usage: "",
                        price: "",
                        discount: "",
                        promise: "",
                        character: ""
                    },
                    demoVideo: "",
                    QnA: ""
                });
                this.editableTabsValue = newTabName;
            }
            if (action === 'remove') {
                let tabs = this.items_data;
                let activeName = this.editableTabsValue;
                if (activeName === targetName) {
                    tabs.forEach((tab, index) => {
                        if (tab.tab_name === targetName) {
                            let nextTab = tabs[index + 1] || tabs[index - 1];
                            if (nextTab) {
                                activeName = nextTab.name;
                            }
                        }
                    });
                }
                this.editableTabsValue = activeName;
                this.items_data = tabs.filter(tab => tab.tab_name !== targetName);
            }
        },
        show() {
            alert("run...")
        },
        formatTooltip(val) {
            return val / 100;
        },
        handleChange(value) {
            console.log(value);
        },
        handleClick(tab, event) {
            console.log(tab, event);
        },
        handleRemove(file, fileList) {
            console.log(file, fileList);
        },
        handlePreview(file) {
            console.log(file);
        },
        onExceed() {
        },
        beforeRemove() {
        },
        handleExceed() {
        },
        connectWS() {
            let _this = this;
            socket = new WebSocket('ws://localhost:10003')
            socket.onopen = function () {
                // console.log('客户端连接上了服务器');
            }
            socket.onmessage = function (e) {
                console.log(" --> " + e.data)
                let data = JSON.parse(e.data)
                _this.live_broadcast = (data.time % 2) === 0
                let liveState = data.liveState
                if (liveState !== undefined) {
                    _this.live_state = liveState
                    if (liveState === 1) {
                        _this.sendSuccessMsg("已开启！")
                    } else if (liveState === 0) {
                        _this.sendSuccessMsg("已关闭！")
                    }
                }
                let voiceList = data.voiceList
                if (voiceList !== undefined) {
                    voice_list = []
                    for (let i = 0; i < voiceList.length; i++) {
                        voice_list[i] = {
                            value: voiceList[i].id,
                            label: voiceList[i].name
                        }
                        _this.voice_list = voice_list
                    }
                }

                let deviceList = data.deviceList
                if (deviceList !== undefined) {
                    device_list = []
                    for (let i = 0; i < deviceList.length; i++) {
                        device_list[i] = {
                            value: deviceList[i],
                            label: deviceList[i]
                        }
                        _this.device_list = device_list
                    }
                }
                let panelMsg = data.panelMsg
                if (panelMsg !== undefined) {
                    _this.panel_msg = panelMsg

                    //Edit by xszyou in 2022/2/3:同步到看板娘
                    text = panelMsg;
                    const tips = document.getElementById("waifu-tips");
                    if (panelMsg != "" && tips != null){
                        sessionStorage.setItem("waifu-text", 8);
                        tips.innerHTML = text;
                        tips.classList.add("waifu-tips-active");
                        messageTimer = setTimeout(() => {
                            sessionStorage.removeItem("waifu-text");
                            tips.classList.remove("waifu-tips-active");
                        }, 7000);
                    }
                    //_this.getMsgList()
                }
                let panelReply = data.panelReply;
                if(panelReply != undefined){
                    _this.addMsg(panelReply)
                }
            }
        },
        getData() {
            let _this = this;
            let url = "http://127.0.0.1:5000/api/get-data";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
            let executed = false
            xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                    try {
                        if (xhr.responseText.length > 0) {
                            let data = await eval('(' + xhr.responseText + ')')
                            let config = data["config"]
                            let source = config["source"]
                            let attribute = config["attribute"]
                            let interact = config["interact"]
                            let perception = interact["perception"]
                            let items = config["items"]
                            _this.play_sound_enabled = interact["playSound"]
                            _this.visualization_detection_enabled = interact["visualization"]
                            _this.source_liveRoom_enabled = source["liveRoom"]["enabled"]
                            _this.source_liveRoom_url = source["liveRoom"]["url"]
                            _this.source_record_enabled = source["record"]["enabled"]
                            _this.source_record_device = source["record"]["device"]
                            _this.attribute_name = attribute["name"]
                            _this.attribute_gender = attribute["gender"]
                            _this.attribute_age = attribute["age"]
                            _this.attribute_birth = attribute["birth"]
                            _this.attribute_zodiac = attribute["zodiac"]
                            _this.attribute_constellation = attribute["constellation"]
                            _this.attribute_job = attribute["job"]
                            _this.attribute_hobby = attribute["hobby"]
                            _this.attribute_contact = attribute["contact"]
                            _this.attribute_voice = attribute["voice"]
                            _this.interact_perception_gift = parseInt(perception["follow"])
                            _this.interact_perception_follow = perception["follow"]
                            _this.interact_perception_join = perception["follow"]
                            _this.interact_perception_chat = perception["follow"]
                            _this.interact_perception_indifferent = perception["follow"]
                            _this.interact_maxInteractTime = interact["maxInteractTime"]
                            _this.interact_QnA = interact["QnA"]
                            let item_data_list = []
                            for (let i = 0; i < items.length; i++) {
                                let item = items[i]
                                let _tab_name = "first"
                                if (i > 0) {
                                    _tab_name = i.toString()
                                }
                                item_data_list[i] = {
                                    tab_name: _tab_name,
                                    enabled: item.enabled,
                                    name: item.name,
                                    explain: {
                                        intro: item.explain.intro,
                                        usage: item.explain.usage,
                                        price: item.explain.price,
                                        discount: item.explain.discount,
                                        promise: item.explain.promise,
                                        character: item.explain.character
                                    },
                                    demoVideo: item.demoVideo,
                                    QnA: item.QnA
                                }
                            }
                            _this.items_data = item_data_list
                            console.log(_this.items_data);
                            executed = true
                        }
                    } catch (e) {
                        console.log(e);
                    }
                }
            }
        },
        postData() {
            let url = "http://127.0.0.1:5000/api/submit";
            let send_data = {
                "config": {
                    "source": {
                        "liveRoom": {
                            "enabled": this.source_liveRoom_enabled,
                            "url": this.source_liveRoom_url
                        },
                        "record": {
                            "enabled": this.source_record_enabled,
                            "device": this.source_record_device
                        }
                    },
                    "attribute": {
                        "voice": this.attribute_voice,
                        "name": this.attribute_name,
                        "gender": this.attribute_gender,
                        "age": this.attribute_age,
                        "birth": this.attribute_birth,
                        "zodiac": this.attribute_zodiac,
                        "constellation": this.attribute_constellation,
                        "job": this.attribute_job,
                        "hobby": this.attribute_hobby,
                        "contact": this.attribute_contact
                    },
                    "interact": {
                        "playSound": this.play_sound_enabled,
                        "visualization": this.visualization_detection_enabled,
                        "QnA": this.interact_QnA,
                        "maxInteractTime": this.interact_maxInteractTime,
                        "perception": {
                            "gift": this.interact_perception_follow,
                            "follow": this.interact_perception_follow,
                            "join": this.interact_perception_follow,
                            "chat": this.interact_perception_follow,
                            "indifferent": this.interact_perception_follow 
                        }
                    },
                    "items": [],
                }
            };
            for (let i = 0; i < this.items_data.length; i++) {
                let item = this.items_data[i]
                send_data.config.items[i] = {
                    enabled: item.enabled,
                    name: item.name,
                    explain: {
                        intro: item.explain.intro,
                        usage: item.explain.usage,
                        price: item.explain.price,
                        discount: item.explain.discount,
                        promise: item.explain.promise,
                        character: item.explain.character
                    },
                    demoVideo: item.demoVideo,
                    QnA: item.QnA
                }
            }
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send('data=' + JSON.stringify(send_data))
            let executed = false
            xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                    try {
                        let data = await eval('(' + xhr.responseText + ')')
                        console.log("data: " + data['result'])
                        executed = true
                    } catch (e) {
                    }
                }
            }
            this.sendSuccessMsg("配置已保存！")
        },

        // async processText() {
        //     try {
        //
        //         const response = await axios.post('http://127.0.0.1:5000/process-text', {
        //             text: this.inputText
        // });
        //
        //     this.outputText = response.data.result;
        //     } catch (error) {
        //     console.error(error);
        //     }
        // },

        // 加载图片
        // getpicture() {
        //     let url = "http://127.0.0.1:5000/receive-image";
        //     // 创建一个新的XMLHttpRequest对象
        //     const xhr = new XMLHttpRequest();
        //     xhr.open("post", url)
        //     xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
        //     xhr.send()
        //     // 监听请求的状态变化
        //     xhr.onreadystatechange = function () {
        //         if (xhr.readyState === 4) {
        //             if (xhr.status === 200) {
        //                 this.picture_url = url;
        //                 console.log(this.picture_url);
        //                 // // 当请求成功时，获取返回的图片数据
        //                 // let imageData = xhr.response;
        //                 //
        //                 // // 将图片数据转换为DataURL
        //                 // let imageBase64 = 'data:image/jpeg;base64,' + btoa(String.fromCharCode(...new Uint8Array(imageData)));
        //                 //
        //                 // // 将DataURL赋值给<img>标签的src属性，以显示图片
        //                 // document.getElementById('image').src = imageBase64;
        //             } else {
        //                 // 当请求失败时，处理错误情况
        //                 console.error('无法获取图片');
        //             }
        //         }
        //     }
        // },


        getPicture() {
            console.log(123);
        },


        // 加载文本
        async getText() {
            try {
                const response = await fetch('http://127.0.0.1:5000/api/get-text', {
                    method: 'GET'
                });

                if (response.ok) {
                    const data = await response.json();
                    const textData = data.text;
                    // const textPlaceholder = document.getElementById('text-placeholder');
                    // textPlaceholder.innerText = textData;
                    console.log(textData)
                    console.log(textData.user_name)
                    this.user_inform.name = textData.user_name;
                    console.log(this.user_inform.user_name);
                    // this.user_inform.gender = textData.user_gender;
                    this.user_inform.gendr = response.data;
                } else {
                    console.error('Failed to fetch the text data.');
                }
            } catch (error) {
                console.error(error);
            }
        },
    //     async getDataFromBackend() {
    //         try {
    //         // 发送异步请求获取后端数据
    //         const response = await axios.get('http://127.0.0.1:5000/api/get-text');
    //
    //         // 更新数据到组件中，实现实时更新
    //         this.user_name = response.data; // 假设后端返回的数据是一个字符串
    //         } catch (error) {
    //             console.error('Failed to get data from backend:', error);
    //         }
    // },

        // 提交用户信息
        postUserInform() {
             let url = "http://127.0.0.1:5000/api/post-user-inform";
             let send_data = {
                  "user_name": this.user_inform.name,
                  "user_gender": this.user_inform.gender,
                  "user_age": this.user_inform.age,
                  "user_type": this.user_inform.type,
                  // "user_med_name":this.user_med_name,
                  // "user_med_spec":this.user_med_spec,
                  // "user_med_usage":this.user_med_usage,
                  // "user_med_freq":this.user_med_freq,
                  // "user_med_dosage":this.user_med_dosage,
                  // "user_med_time":this.user_med_time
             }
             let xhr = new XMLHttpRequest()
             xhr.open("post", url)
             xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
             xhr.send('data=' + JSON.stringify(send_data))
             let executed = false
             xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                    try {
                       let data = JSON.parse(xhr.responseText);
                       console.log("data: " + data['result']);
                        executed = true;
                    } catch (e) {
                    }
                }
            }
        },


        getLocation() {
            let url = "http://127.0.0.1:5000/api/get-location";
            let xhr = new XMLHttpRequest();
            xhr.open("get", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
            let executed = false
            xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                    let location = eval("location");
                    console.log(location);
                    this.attribute_location = location;
                }
            }
        },

        postLocation() {
            let url = "http://127.0.0.1:5000/api/post-location";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
        },

        postStartLive() {
            this.postData()
            this.live_state = 2
            let url = "http://127.0.0.1:5000/api/start-live";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
        },


        postStopLive() {
            this.live_state = 3
            let url = "http://127.0.0.1:5000/api/stop-live";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
            
        },
        postControlEyes() {
            let url = "http://127.0.0.1:5000/api/control-eyes";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
            if(this.visualization_detection_enabled){
                this.visualization_detection_enabled = false
            }else{
                this.visualization_detection_enabled = true
            }
        },
        isEmptyItem(data) {
            let isEmpty = true
            let explain = data["explain"]
            for (let key in data) {
                let value = data[key]
                if (key !== "tab_name" && value.constructor === String && value.length > 0) {
                    isEmpty = false
                    break
                }
            }
            for (let key in explain) {
                let value = explain[key]
                if (value.constructor === String && value.length > 0) {
                    isEmpty = false
                    break
                }
            }
            return isEmpty
        },
        lastItemIsEmpty() {
            return this.isEmptyItem(this.items_data[this.items_data.length - 1])
        },
        uuid() {
            let uuid = Math.random().toString(36);
            return uuid
        },
        runnnable() {
            setTimeout(() => {
                let _this = this
                let item_data_list = []
                let changed = false
                let index = 0
                for (let i = 0; i < _this.items_data.length; i++) {
                    let data = _this.items_data[i]
                    if (i === (_this.items_data.length - 1) || !this.isEmptyItem(data)) {
                        item_data_list[index] = _this.items_data[i]
                        index++
                    } else {
                        changed = true
                    }
                }
                if (!this.lastItemIsEmpty()) {
                    changed = true
                    item_data_list.push({
                        tab_name: this.uuid(),
                        enabled: false,
                        name: "",
                        explain: {
                            intro: "",
                            usage: "",
                            price: "",
                            discount: "",
                            promise: "",
                            character: ""
                        },
                        demoVideo: "",
                        QnA: ""
                    })
                }
                if (changed) {
                    _this.items_data = item_data_list
                    console.log("修改了！" + _this.items_data.length)
                }
                this.runnnable()
            }, 50)
        },
        sendSuccessMsg(text) {
            this.$notify({
                title: '成功',
                message: text,
                type: 'success'
            });
        },
        send(sendto) {
            let _this = this;
            let text = _this.send_msg;
            if (!text) {
                alert('请输入内容');
                return;
            }
            let info = {
                'content' : text ,
                'timetext' : _this.getCurrentTime() ,
                'type' : 'member' ,
                'way' : 'send'
            }
            console.log(text)
            _this.msg_list.push(info);
            this.timer = setTimeout(()=>{   //设置延迟执行
                //滚动条置底
               let height = document.querySelector('.content').scrollHeight;
               document.querySelector(".content").scrollTop = height;
           },1000)
            _this.send_msg = ''
            let url = "http://127.0.0.1:5000/api/send";
            let send_data = {
                "msg": text,
                "sendto" : sendto
            };

            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/json")
            xhr.send(JSON.stringify(send_data));
            let executed = false
            xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                  // _this.getMsgList()
                //    document.querySelector('#textarea').value = '';
                //    document.querySelector('#textarea').focus();

                }
            }

            // // text = text.replace(/\s/g, "<br/>");
            // text = text.replace(/\n/g, "<br/>");
            // text = text.replace(/\r\n/g, "<br/>");
            // let item = document.createElement('div');
            // item.className = 'item item-right';
            // item.innerHTML = `<div class="bubble bubble-right">${text}</div><div class="avatar"><img src="static/from.jpg" /></div>`;
            // document.querySelector('.content').appendChild(item);
            // document.querySelector('#textarea').value = '';
            // document.querySelector('#textarea').focus();
            // //滚动条置底
            // let height = document.querySelector('.content').scrollHeight;
            // document.querySelector(".content").scrollTop = height;
        },
        getMsgList(){
            let _this = this;
            let url = "http://127.0.0.1:5000/api/get-msg";
            let xhr = new XMLHttpRequest()
            xhr.open("post", url)
            xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
            xhr.send()
            let executed = false
            xhr.onreadystatechange = async function () {
                if (!executed && xhr.status === 200) {
                    try {
                        if (xhr.responseText.length > 0) {
                            let data = await eval('(' + xhr.responseText + ')')
                            _this.msg_list = data['list'];
                               
                            //滚动条置底
                            let height = document.querySelector('.content').scrollHeight;
                            document.querySelector(".content").scrollTop = height;
                            this.timer = setTimeout(()=>{   //设置延迟执行
                                //滚动条置底
                               let height = document.querySelector('.content').scrollHeight;
                               document.querySelector(".content").scrollTop = height;
                           },1000)
                        }
                    } catch (e) {
                        console.log(e);
                    }
                }
            }
        },
        addMsg(data){get
            let _this = this;
            let info = {
                'content' : data['content'] ,
                'timetext' :  _this.getCurrentTime() ,
                'type' : data['type'] ,
                'way' : 'send' 
            } 
            _this.msg_list.push(info);
            
            this.timer = setTimeout(()=>{   //设置延迟执行
                 //滚动条置底
                let height = document.querySelector('.content').scrollHeight;
                document.querySelector(".content").scrollTop = height;
            },1000)
             

        },
        getCurrentTime() {
            //获取当前时间并打印
            var _this = this;
            let yy = new Date().FullYear();
            let mm = new Date().getMonth()+1<10 ? '0'+parseInt(new Date().getMonth()+1) : new Date().getMonth()+1;
            let dd = new Date().getDate()<10 ? '0'+new Date().getDate() : new Date().getDate();
            let hh = new Date().getHours()<10 ? '0'+new Date().getHours() : new Date().getHours();
            let mf = new Date().getMinutes()<10 ? '0'+new Date().getMinutes() : new Date().getMinutes();
            let ss = new Date().getSeconds()<10 ? '0'+new Date().getSeconds() : new Date().getSeconds();
            let gettime = yy+'-'+mm+'-'+dd+' '+hh+':'+mf+':'+ss;
            return gettime;
           
        }

    },
    mounted() {
        let _this = this;
        _this.getData();
        _this.getMsgList();
        _this.connectWS();

        // _this.runnnable()
        // _this.items_data.push({});
    },
    watch: {
        items_data() {
            // console.log("items_data 改变了");
        }
    }
})