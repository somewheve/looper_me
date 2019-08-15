<template>
  <div class="changePsd" :style="height">
    <el-col :xs="20" :sm="10" :md="8">
      <el-row>
        <el-col :span="24">
          <el-form label-position="right" label-width="80px" :model="formPsd">
            <el-form-item label="原密码">
              <el-input
                type="password"
                show-password
                v-model="formPsd.old_pwd"
                placeholder="请输入原密码"
              ></el-input>
            </el-form-item>
            <el-form-item label="新密码">
              <el-input
                type="password"
                show-password
                v-model="formPsd.new_pwd1"
                placeholder="请输入新密码"
              ></el-input>
            </el-form-item>
            <el-form-item label="再次输入">
              <el-input
                type="password"
                show-password
                v-model="formPsd.new_pwd2"
                placeholder="请再次输入新密码"
                @keyup.enter.native="onSubmit()"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="onSubmit()">立即修改</el-button>
              <el-button @click="resetForm()">重置</el-button>
            </el-form-item>
          </el-form>
        </el-col>
      </el-row>
    </el-col>
  </div>
</template>
<script>
import { setTimeout } from "timers";
export default {
  name: "changePassword",
  data() {
    return {
      token: "",
      changePsdURL: this.URL + "/change_pwd",
      height: {
        height: ""
      },
      formPsd: {
        old_pwd: "",
        new_pwd1: "",
        new_pwd2: ""
      }
    };
  },
  methods: {
    onSubmit() {
      if (
        this.formPsd.old_pwd == "" ||
        this.formPsd.new_pwd1 == "" ||
        this.formPsd.new_pwd2 == ""
      ) {
        return this.$message({
          showClose: true,
          message: "必填内容不能为空!",
          type: "error"
        });
      }
      if (this.formPsd.old_pwd == this.formPsd.new_pwd1) {
        return this.$message({
          showClose: true,
          message: "原密码与新密码一致!",
          type: "error"
        });
      }
      if (this.formPsd.new_pwd1 !== this.formPsd.new_pwd2) {
        return this.$message({
          showClose: true,
          message: "新密码和再次输入的密码不一致!",
          type: "error"
        });
      }

      this.axios
        .post(this.changePsdURL, this.$qs.stringify(this.formPsd), {
          headers: {
            Authorization: "JWT " + this.token
          }
        })
        .then(data => {
          let returnData = data.data;
          console.log(returnData);
          if (returnData.success == true) {
            this.$message({
              showClose: true,
              message: returnData.msg,
              type: "success"
            });
            setTimeout(() => {
              this.logout();
              sessionStorage.removeItem("token");
            }, 1000);
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
    resetForm() {
      this.formPsd.old_pwd = "";
      this.formPsd.new_pwd1 = "";
      this.formPsd.new_pwd2 = "";
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    },
    setBoxHeight() {
      let h = window.innerHeight - 50;
      this.height.height = h + "px";
      window.onresize = () => {
        this.setBoxHeight();
      };
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
    this.setBoxHeight();
  }
};
</script>
<style>
.changePsd {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  padding-top: 100px;
  box-sizing: border-box;
}
.changePsd label {
  font-weight: 400;
}
</style>
