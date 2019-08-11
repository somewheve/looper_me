<template>
  <div class="fullScreen">
    <el-col :span="12">
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <img src="@/assets/image/forum.png" alt="" style="width:100%">
          </div>
        </el-col>
        <el-col :span="8">
          <div class="grid-content bg-purple">
            <img src="@/assets/image/document.png" alt="" style="width:100%">
          </div>
        </el-col>
         <el-col :span="8">
          <div class="grid-content bg-purple">
            <img src="@/assets/image/qq.png" alt="" style="width:100%">
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
    return {};
  }
};
</script>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-col {
  border-radius: 4px;
}

.bg-purple {
  /* background: #eee; */
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
  margin-top: 100px;
}
.icon {
  color: black;
  font-size: 20px;
}
</style>
