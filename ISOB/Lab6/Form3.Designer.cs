namespace Lab6
{
    partial class Form3
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }


        private List<TextBox> messageFields = new();
        private List<Button> signOutButtons = new();
        private List<Button> sendButtons = new();
        private List<Label> usernameLabels = new();





		#region Windows Form Designer generated code

		/// <summary>
		///  Required method for Designer support - do not modify
		///  the contents of this method with the code editor.
		/// </summary>
		/// 
		private void InitializeComponent()
		{
			SignIn1 = new Button();
			Message1 = new TextBox();
			MessagesListBox = new ListBox();
			Login1 = new TextBox();
			Password1 = new TextBox();
			Send1 = new Button();
			AttackDefensesCheckedListBox = new CheckedListBox();
			SignOut1 = new Button();
			SignOut2 = new Button();
			Send2 = new Button();
			Message2 = new TextBox();
			SignOut3 = new Button();
			Send3 = new Button();
			Message3 = new TextBox();
			SignOut4 = new Button();
			Send4 = new Button();
			Message4 = new TextBox();
			label1 = new Label();
			label2 = new Label();
			Username1 = new Label();
			Username2 = new Label();
			Username3 = new Label();
			Username4 = new Label();
			SuspendLayout();
			// 
			// SignIn1
			// 
			SignIn1.Location = new Point(410, 86);
			SignIn1.Margin = new Padding(3, 4, 3, 4);
			SignIn1.Name = "SignIn1";
			SignIn1.Size = new Size(242, 30);
			SignIn1.TabIndex = 2;
			SignIn1.Text = "Enter";
			SignIn1.UseVisualStyleBackColor = true;
			SignIn1.Click += SignIn_Click;
			// 
			// Message1
			// 
			Message1.Location = new Point(150, 78);
			Message1.Margin = new Padding(3, 4, 3, 4);
			Message1.Name = "Message1";
			Message1.Size = new Size(191, 27);
			Message1.TabIndex = 3;
			Message1.Visible = false;
			// 
			// MessagesListBox
			// 
			MessagesListBox.FormattingEnabled = true;
			MessagesListBox.Location = new Point(715, 34);
			MessagesListBox.Margin = new Padding(3, 4, 3, 4);
			MessagesListBox.Name = "MessagesListBox";
			MessagesListBox.Size = new Size(309, 324);
			MessagesListBox.TabIndex = 4;
			// 
			// Login1
			// 
			Login1.Location = new Point(410, 53);
			Login1.Margin = new Padding(3, 4, 3, 4);
			Login1.Name = "Login1";
			Login1.Size = new Size(114, 27);
			Login1.TabIndex = 0;
			// 
			// Password1
			// 
			Password1.Location = new Point(539, 53);
			Password1.Margin = new Padding(3, 4, 3, 4);
			Password1.Name = "Password1";
			Password1.Size = new Size(114, 27);
			Password1.TabIndex = 1;
			// 
			// Send1
			// 
			Send1.Location = new Point(50, 34);
			Send1.Margin = new Padding(3, 4, 3, 4);
			Send1.Name = "Send1";
			Send1.Size = new Size(94, 30);
			Send1.TabIndex = 25;
			Send1.Text = "Send";
			Send1.UseVisualStyleBackColor = true;
			Send1.Visible = false;
			Send1.Click += Se_C;
			// 
			// AttackDefensesCheckedListBox
			// 
			AttackDefensesCheckedListBox.FormattingEnabled = true;
			AttackDefensesCheckedListBox.Items.AddRange(new object[] { "Privileges minimization", "Buffer overflow", "DoS", "XSS" });
			AttackDefensesCheckedListBox.Location = new Point(410, 143);
			AttackDefensesCheckedListBox.Margin = new Padding(3, 4, 3, 4);
			AttackDefensesCheckedListBox.Name = "AttackDefensesCheckedListBox";
			AttackDefensesCheckedListBox.Size = new Size(243, 114);
			AttackDefensesCheckedListBox.TabIndex = 31;
			// 
			// SignOut1
			// 
			SignOut1.Location = new Point(50, 73);
			SignOut1.Margin = new Padding(3, 4, 3, 4);
			SignOut1.Name = "SignOut1";
			SignOut1.Size = new Size(94, 30);
			SignOut1.TabIndex = 32;
			SignOut1.Text = "Exit";
			SignOut1.UseVisualStyleBackColor = true;
			SignOut1.Visible = false;
			SignOut1.Click += SignOut_Click;
			// 
			// SignOut2
			// 
			SignOut2.Location = new Point(50, 163);
			SignOut2.Margin = new Padding(3, 4, 3, 4);
			SignOut2.Name = "SignOut2";
			SignOut2.Size = new Size(94, 30);
			SignOut2.TabIndex = 35;
			SignOut2.Text = "Exit";
			SignOut2.UseVisualStyleBackColor = true;
			SignOut2.Visible = false;
			SignOut2.Click += SignOut_Click;
			// 
			// Send2
			// 
			Send2.Location = new Point(50, 125);
			Send2.Margin = new Padding(3, 4, 3, 4);
			Send2.Name = "Send2";
			Send2.Size = new Size(94, 30);
			Send2.TabIndex = 34;
			Send2.Text = "Send";
			Send2.UseVisualStyleBackColor = true;
			Send2.Visible = false;
			Send2.Click += Se_C;
			// 
			// Message2
			// 
			Message2.Location = new Point(150, 169);
			Message2.Margin = new Padding(3, 4, 3, 4);
			Message2.Name = "Message2";
			Message2.Size = new Size(191, 27);
			Message2.TabIndex = 33;
			Message2.Visible = false;
			// 
			// SignOut3
			// 
			SignOut3.Location = new Point(50, 254);
			SignOut3.Margin = new Padding(3, 4, 3, 4);
			SignOut3.Name = "SignOut3";
			SignOut3.Size = new Size(94, 30);
			SignOut3.TabIndex = 38;
			SignOut3.Text = "Exit";
			SignOut3.UseVisualStyleBackColor = true;
			SignOut3.Visible = false;
			SignOut3.Click += SignOut_Click;
			// 
			// Send3
			// 
			Send3.Location = new Point(50, 216);
			Send3.Margin = new Padding(3, 4, 3, 4);
			Send3.Name = "Send3";
			Send3.Size = new Size(94, 30);
			Send3.TabIndex = 37;
			Send3.Text = "Send";
			Send3.UseVisualStyleBackColor = true;
			Send3.Visible = false;
			Send3.Click += Se_C;
			// 
			// Message3
			// 
			Message3.Location = new Point(150, 260);
			Message3.Margin = new Padding(3, 4, 3, 4);
			Message3.Name = "Message3";
			Message3.Size = new Size(191, 27);
			Message3.TabIndex = 36;
			Message3.Visible = false;
			// 
			// SignOut4
			// 
			SignOut4.Location = new Point(50, 342);
			SignOut4.Margin = new Padding(3, 4, 3, 4);
			SignOut4.Name = "SignOut4";
			SignOut4.Size = new Size(94, 30);
			SignOut4.TabIndex = 41;
			SignOut4.Text = "Exit";
			SignOut4.UseVisualStyleBackColor = true;
			SignOut4.Visible = false;
			SignOut4.Click += SignOut_Click;
			// 
			// Send4
			// 
			Send4.Location = new Point(50, 303);
			Send4.Margin = new Padding(3, 4, 3, 4);
			Send4.Name = "Send4";
			Send4.Size = new Size(94, 30);
			Send4.TabIndex = 40;
			Send4.Text = "Send";
			Send4.UseVisualStyleBackColor = true;
			Send4.Visible = false;
			Send4.Click += Se_C;
			// 
			// Message4
			// 
			Message4.Location = new Point(150, 342);
			Message4.Margin = new Padding(3, 4, 3, 4);
			Message4.Name = "Message4";
			Message4.Size = new Size(191, 27);
			Message4.TabIndex = 39;
			Message4.Visible = false;
			// 
			// label1
			// 
			label1.AutoSize = true;
			label1.Location = new Point(410, 29);
			label1.Margin = new Padding(2, 0, 2, 0);
			label1.Name = "label1";
			label1.Size = new Size(75, 20);
			label1.TabIndex = 42;
			label1.Text = "Username";
			// 
			// label2
			// 
			label2.AutoSize = true;
			label2.Location = new Point(539, 29);
			label2.Margin = new Padding(2, 0, 2, 0);
			label2.Name = "label2";
			label2.Size = new Size(70, 20);
			label2.TabIndex = 43;
			label2.Text = "Password";
			// 
			// Username1
			// 
			Username1.AutoSize = true;
			Username1.Location = new Point(151, 45);
			Username1.Margin = new Padding(2, 0, 2, 0);
			Username1.Name = "Username1";
			Username1.Size = new Size(0, 20);
			Username1.TabIndex = 44;
			// 
			// Username2
			// 
			Username2.AutoSize = true;
			Username2.Location = new Point(150, 135);
			Username2.Margin = new Padding(2, 0, 2, 0);
			Username2.Name = "Username2";
			Username2.Size = new Size(0, 20);
			Username2.TabIndex = 45;
			// 
			// Username3
			// 
			Username3.AutoSize = true;
			Username3.Location = new Point(150, 226);
			Username3.Margin = new Padding(2, 0, 2, 0);
			Username3.Name = "Username3";
			Username3.Size = new Size(0, 20);
			Username3.TabIndex = 46;
			// 
			// Username4
			// 
			Username4.AutoSize = true;
			Username4.Location = new Point(150, 314);
			Username4.Margin = new Padding(2, 0, 2, 0);
			Username4.Name = "Username4";
			Username4.Size = new Size(0, 20);
			Username4.TabIndex = 47;
			// 
			// Form3
			// 
			AutoScaleDimensions = new SizeF(8F, 20F);
			AutoScaleMode = AutoScaleMode.Font;
			BackColor = Color.Silver;
			ClientSize = new Size(1070, 405);
			Controls.Add(Username4);
			Controls.Add(Username3);
			Controls.Add(Username2);
			Controls.Add(Username1);
			Controls.Add(label2);
			Controls.Add(label1);
			Controls.Add(SignOut4);
			Controls.Add(Send4);
			Controls.Add(Message4);
			Controls.Add(SignOut3);
			Controls.Add(Send3);
			Controls.Add(Message3);
			Controls.Add(SignOut2);
			Controls.Add(Send2);
			Controls.Add(Message2);
			Controls.Add(SignOut1);
			Controls.Add(AttackDefensesCheckedListBox);
			Controls.Add(Send1);
			Controls.Add(MessagesListBox);
			Controls.Add(Message1);
			Controls.Add(SignIn1);
			Controls.Add(Password1);
			Controls.Add(Login1);
			Margin = new Padding(3, 4, 3, 4);
			Name = "Form3";
			Text = "Form1";
			Load += Form3_Load;
			ResumeLayout(false);
			PerformLayout();
		}

		#endregion
		private Button SignIn1;
        private TextBox Message1;
        private ListBox MessagesListBox;
        private TextBox Login1;
        private TextBox Password1;
        private Button Send1;
        private CheckedListBox AttackDefensesCheckedListBox;
        private Button SignOut1;
        private Button SignOut2;
        private Button Send2;
        private TextBox Message2;
        private Button SignOut3;
        private Button Send3;
        private TextBox Message3;
        private Button SignOut4;
        private Button Send4;
        private TextBox Message4;
        private Label label1;
        private Label label2;
        private Label Username1;
        private Label Username2;
        private Label Username3;
        private Label Username4;
    }
}
