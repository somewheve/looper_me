<template>
  <div style="padding:30px;" class="config">
    <table>
      <tr>
        <th>配置项</th>
        <th>状态</th>
      </tr>
      <tr>
        <td>AUTH_REQUIRED</td>
        <td>
          <el-switch v-model="AUTH_REQUIRED"></el-switch>
        </td>
      </tr>
      <tr>
        <td>KEY</td>
        <td>
          <el-input v-model="KEY" placeholder="请输入KEY"></el-input>
        </td>
      </tr>
      <tr>
        <td>ORIGIN_NUMBER</td>
        <td>
          <el-input v-model="ORIGIN_NUMBER" placeholder="请输入ORIGIN_NUMBER"></el-input>
        </td>
      </tr>
    </table>
    <el-button
      type="success"
      icon="el-icon-check"
      @click="onSubmit(AUTH_REQUIRED,KEY,ORIGIN_NUMBER)"
    >保存</el-button>
  </div>
</template>
<script>
export default {
  inject: ["reload"],
  data() {
    return {
      AUTH_REQUIRED: false,
      KEY: "",
      ORIGIN_NUMBER: "",
      configURL: this.URL + "/config_manage"
    };
  },
  methods: {
    getConfigData() {
      this.axios({
        url: this.configURL,
        methods: "get"
      })
        .then(data => {
          let returnData = data.data.data;
          this.AUTH_REQUIRED = returnData.AUTH_REQUIRED == 1 ? true : false;
          this.KEY = returnData.KEY;
          this.ORIGIN_NUMBER = returnData.ORIGIN_NUMBER;
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit(AUTH_REQUIRED, KEY, ORIGIN_NUMBER) {
      let flag = AUTH_REQUIRED == true ? 1 : 0;
      if (KEY == "" || ORIGIN_NUMBER == "") {
        return this.$message({
          message: "内容不能为空!",
          type: "error"
        });
      }
      let sendData = {
        AUTH_REQUIRED: flag,
        KEY: KEY,
        ORIGIN_NUMBER: ORIGIN_NUMBER
      };
      this.axios
        .post(this.configURL, this.$qs.stringify(sendData))
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.$message({
              message: returnData.msg,
              type: "success"
            });
            setTimeout(() => {
              this.reload();
            }, 1500);
          }
        })
        .catch(err => {
          console.log(err);
        });
    }
  },
  mounted() {
    this.getConfigData();
  }
};
</script>
<style scoped>
.config table {
  width: 100%;
  border-collapse: collapse;
}
.config table tr th,
.config table tr td {
  color: #909399;
  width: 50%;
  text-align: left;
  border: 1px solid #ebeef5;
  padding: 15px;
  font-size: 14px;
}
.config table tr th {
  color: #909399;
}
.config table tr td {
  color: #606266;
}
</style>
<style>
.config .el-button--success {
  margin-top: 20px;
  float: right;
}
</style>
