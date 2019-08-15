<template>
  <div class="fullScreen" :style="height">
    <el-col :xs="24" :sm="18" :md="10">
      <el-row :gutter="40">
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <a href="http://47.93.26.201:3000" target="_blank">
              <img src="@/assets/image/forum.png" alt style="width:100%" />
              <p class="iconTitle">论坛</p>
            </a>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <a href="#" target="_blank" type="primary">
              <img src="@/assets/image/document.png" alt style="width:100%" />
              <p class="iconTitle">文档</p>
            </a>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <a href="https://jq.qq.com/?_wv=1027&k=5BxlYeB" target="_blank" type="primary">
              <img src="@/assets/image/qq.png" alt style="width:100%" />
              <p class="iconTitle">交流</p>
            </a>
          </div>
        </el-col>
      </el-row>
    </el-col>
  </div>
</template>

<script>
export default {
  name: "Dashboard",
  data() {
    return {
      token: "",
      height: {
        height: ""
      }
    };
  },
  methods: {
    setBoxHeight() {
      let h = window.innerHeight - 50;
      this.height.height = h + "px";
      window.onresize = () => {
        this.setBoxHeight();
      };
    },
    async logout() {
      await this.$store.dispatch("user/logout");
      this.$router.push(`/login?redirect=${this.$route.fullPath}`);
    }
  },
  mounted() {
    this.token = sessionStorage.getItem("token");
    if (this.token == "") {
      this.logout();
    }
    this.setBoxHeight();
  }
};
</script>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 5px;
}

.bg-purple {
  background: #e8e8e8;
  padding: 10px 20px;
  cursor: pointer;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.fullScreen {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.iconTitle {
  text-align: center;
  margin-top: 20px;
  font-size: 16px;
  color: #304156;
}
</style>
