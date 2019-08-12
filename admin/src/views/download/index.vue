<template>
  <div class="symbolDetail">
    <h3>{{symbol}}</h3>
    <div class="block">
      <span class="demonstration">选择时间段:</span>
      <el-date-picker
        v-model="time"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
      ></el-date-picker>
    </div>
    <div class="downloadBtn">
      <el-button-group>
        <el-button type="primary" size="medium" @click="download('timeDownload',time)">
          指定时间段下载
          <i class="el-icon-download el-icon--right"></i>
        </el-button>
        <el-button type="success" size="medium" @click="download('singleVarietyDownload')">
           单品种下载
          <i class="el-icon-download el-icon--right"></i>
        </el-button>
        <el-button type="warning" size="medium" @click="download('seriesDownload')">
           同系列下载
          <i class="el-icon-download el-icon--right"></i>
        </el-button>
      </el-button-group>
    </div>
  </div>
</template>

<script>
export default {
  name: "download",
  data() {
    return {
      downloadURL: this.URL + "/file",
      symbol: "",
      time: ""
    };
  },
  created() {
    this.symbol = this.$route.query.symbolName;
  },
  methods: {
    FormattingTime(value) {
      let date = new Date(value);
      let y = date.getFullYear();
      let MM = date.getMonth() + 1;
      MM = MM < 10 ? "0" + MM : MM;
      let d = date.getDate();
      d = d < 10 ? "0" + d : d;
      return y + "-" + MM + "-" + d;
    },
    download(type, time = "") {
      let start;
      let end;
      let filename;
      let code;

      let symbolArr = JSON.parse(sessionStorage.getItem("symbolArr"));
      let a = this.symbol.split(".");
      let reg = /[0-9]+$/gi;
      let seriesSymbol = a[0].replace(a[0].match(reg)[0], "");
      let seriesArr = symbolArr.filter(item => {
        return item.includes(seriesSymbol);
      });

      if (type == "timeDownload") {
        if (time == "") {
          return this.$message.error("请选择时间段!");
        }
        start = this.FormattingTime(time[0]);
        end = this.FormattingTime(time[1]);
        code = [this.symbol];
        filename = this.symbol + "_" + start + "_" + end + ".csv";
      } else if (type == "singleVarietyDownload") {
        start = "";
        end = "";
        code = [this.symbol];
        filename = this.symbol + ".csv";
      } else {
        start = "";
        end = "";
        code = seriesArr;
        filename = seriesSymbol + "同系列.csv";
      }

      let sendData = {
        code: code.join("+"),
        start: start,
        end: end
      };
      
      this.axios
        .post(this.downloadURL, this.$qs.stringify(sendData), {
          responseType: "blob"
        })
        .then(data => {
          let blob = data.data;
          let reader = new FileReader();
          reader.readAsDataURL(blob);
          reader.onload = e => {
            let a = document.createElement("a");
            a.download = filename;
            a.href = e.target.result;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
          };
        })
        .catch(err => {
          console.log(err);
        });
    }
  }
};
</script>

<style scoped>
.symbolDetail {
  margin: 60px auto 0;
  text-align: center;
}
.symbolDetail h3 {
  text-align: center;
  margin-bottom: 50px;
  font-family: manaco;
  font-weight: 300;
  font-size: 30px;
}
.block {
  margin-top: 30px;
}
.downloadBtn {
  margin-top: 50px;
}
.block span.demonstration {
  font-family: manaco;
}
</style>

<style>
  /* 覆盖element-ui的样式（注意：此处不能加scope,否则无效）*/
  .symbolDetail .el-date-editor .el-range-separator {
    padding: 0;
  }
</style>
