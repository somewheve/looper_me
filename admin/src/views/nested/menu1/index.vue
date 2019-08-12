<template>
  <div style="padding:30px;" class="config">
    <table>
      <tr>
        <th>配置项</th>
        <th>状态</th>
      </tr>
      <tr>
        <td>auth_required</td>
        <td>
          <el-switch v-model="auth_required"></el-switch>
        </td>
      </tr>
      <tr>
        <td>key</td>
        <td>
          <el-input v-model="key" placeholder="请输入key"></el-input>
        </td>
      </tr>
      <tr>
        <td>origin_number</td>
        <td>
          <el-input v-model="origin_number" placeholder="请输入origin_number"></el-input>
        </td>
      </tr>
    </table>
    <el-button
      type="success"
      icon="el-icon-check"
      @click="onSubmit(auth_required,key,origin_number)"
    >保存</el-button>
  </div>
</template>
<script>
export default {
  inject: ["reload"],
  data() {
    return {
      auth_required: false,
      key: "",
      origin_number: "",
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
          this.auth_required = returnData.auth_required == 1 ? true : false;
          this.key = returnData.key;
          this.origin_number = returnData.origin_number;
        })
        .catch(err => {
          console.log(err);
        });
    },
    onSubmit(auth_required, key, origin_number) {
      let flag = auth_required == true ? 1 : 0;
      if (key == "" || origin_number == "") {
        return this.$message({
          message: "内容不能为空!",
          type: "error"
        });
      }
      let sendData = {
        auth_required: flag,
        key: key,
        origin_number: origin_number
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
