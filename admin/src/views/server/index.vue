<template>
  <div class="ipTab">
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column type="index"></el-table-column>
      <el-table-column prop="ip" label="ip地址"></el-table-column>
      <el-table-column prop="address" label="操作">
        <template slot-scope="scope">
          <el-button size="mini" type="danger" @click="prohibition(scope.row)">封禁</el-button>
          <el-button size="mini" type="success" @click="pullBlack(scope.row)">拉黑</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  inject: ["reload"],
  data() {
    return {
      token: "",
      originURL: this.URL + "/origin_manage",
      tableData: []
    };
  },
  methods: {
    getOriginURLData() {
      this.axios
        .get(this.originURL, {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.tableData = returnData.data;
          } else if (returnData.success == false && returnData.token == false) {
            setTimeout(() => {
              this.$message({
                message: "登录信息已过期,请重新登录!",
                type: "error"
              });
              this.logout();
              sessionStorage.removeItem("token");
            }, 100);
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    prohibition(row) {
      let sendData = {
        todo: "kill",
        ip: row.ip
      };
      this.axios
        .post(this.originURL, this.$qs.stringify(sendData), {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.$message({
              message: returnData.msg,
              type: "success",
              center: true
            });
            setTimeout(() => {
              this.reload();
            }, 1500);
          } else if (returnData.success == false && returnData.token == false) {
            setTimeout(() => {
              this.$message({
                message: "登录信息已过期,请重新登录!",
                type: "error"
              });
              this.logout();
              sessionStorage.removeItem("token");
            }, 100);
          } else {
            this.$message({
              showClose: true,
              message: returnData.msg,
              type: "error"
            });
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    pullBlack(row) {
      let sendData = {
        todo: "pull_black",
        ip: row.ip
      };
      this.axios
        .post(this.originURL, this.$qs.stringify(sendData), {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          if (returnData.success == true) {
            this.$message({
              message: returnData.msg,
              type: "success",
              center: true
            });
            setTimeout(() => {
              this.reload();
            }, 1500);
          } else if (returnData.success == false && returnData.token == false) {
            setTimeout(() => {
              this.$message({
                message: "登录信息已过期,请重新登录!",
                type: "error"
              });
              this.logout();
              sessionStorage.removeItem("token");
            }, 100);
          } else {
            this.$message({
              showClose: true,
              message: returnData.msg,
              type: "error"
            });
          }
        })
        .catch(err => {
          console.log(err);
        });
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
    this.getOriginURLData();
  }
};
</script>

<style scoped>
.ipTab {
  padding: 20px;
}
</style>
