# 🚀 快速启动指南

## 5 分钟安装测试

### 步骤 1: 生成图标 (1 分钟)

```bash
cd rustchain-wallet-extension
npm install
npm run generate-icons
```

**或者** 手动创建占位图标：
- 复制 `icons/icon.svg` 并重命名为 `icon16.png`, `icon48.png`, `icon128.png`
- 或使用任何 128x128 PNG 图片临时替代

### 步骤 2: 加载到 Chrome (1 分钟)

1. 打开 Chrome 浏览器
2. 访问 `chrome://extensions/`
3. 右上角开启"开发者模式"
4. 点击"加载已解压的扩展程序"
5. 选择 `rustchain-wallet-extension` 文件夹
6. ✅ 扩展已安装！

### 步骤 3: 创建钱包 (2 分钟)

1. 点击浏览器工具栏的 RustChain 螃蟹图标 🦀
2. 输入密码（至少 8 位）
3. 点击"Create Wallet"
4. ⚠️ **重要**: 抄下 24 个单词，保存到安全地方
5. 点击"I've Backed It Up"
6. ✅ 钱包创建完成！

### 步骤 4: 测试功能 (1 分钟)

- **查看地址**: 主界面显示你的 RTC 地址
- **复制地址**: 点击 📋 复制按钮
- **锁定钱包**: 设置 → Lock Wallet
- **解锁钱包**: 输入密码解锁

## 测试加密功能（可选）

在浏览器中打开 `test-crypto.html`：

```bash
# macOS/Linux
open test-crypto.html

# Windows
start test-crypto.html
```

点击各个测试按钮验证加密功能正常。

## 常见问题

### Q: 图标不显示？
A: 确保生成了 PNG 文件：
```bash
npm install
npm run generate-icons
```

### Q: 点击没反应？
A: 打开开发者工具检查错误：
- 右键扩展图标 → "检查"
- 查看 Console 标签

### Q: 如何重置钱包？
A: 卸载扩展并重新加载：
1. `chrome://extensions/` → 移除扩展
2. 重新点击"加载已解压的扩展程序"

### Q: 助记词丢了怎么办？
A: **无法恢复！** 必须重新创建钱包。务必备份助记词。

## 下一步

- ✅ 完成基础功能测试
- 📸 准备截图
- 🎥 录制演示视频（可选）
- 📤 提交到 GitHub
- 💰 申请 40 RTC 奖励

## 提交奖励

完成测试后，参考 `COMPLETION_REPORT.md` 提交到 Issue #730。

---

**需要帮助？**
- 查看 `README.md` 了解详细功能
- 查看 `INSTALL.md` 了解完整安装指南
- Discord: https://discord.gg/VqVVS2CW9Q

🦀 Happy Wallet Testing!
