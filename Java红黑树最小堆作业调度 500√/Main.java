
import java.util.ArrayList;
import java.io.*;

public class Main {
    public int globletime;
    public static HeapMin heap;
    public static RBTree<Job> rbt;
    public static Scheduler scheduler;
    public static Processor processor;
    public static ArrayList<String> rawcommands=new ArrayList<String>();
    public static ArrayList<Command> commands=new ArrayList<Command>();
    public static ArrayList<Job> tempjoblist= new ArrayList<Job>();
    public static String outputpath="output_file.txt";
    public static boolean creatTxtFile(String path) throws IOException {
        boolean flag = false;
        File filename = new File(path);
        if (!filename.exists()) {
            filename.createNewFile();
            flag = true;
        }
        return flag;
    }
    public HeapMin newheap(){
        return new HeapMin(1000);
    }
    public RBTree newrbt(){
        return new RBTree();
    }
    public Scheduler newscheduler(){
        return new Scheduler();
    }
    public Processor newprocessor(){
        return new Processor(0,null);
    }
    public static void writeToFile(String s){
        try {
            File file = new File(outputpath);
            if(file.exists()){
                FileWriter fw = new FileWriter(file,true);
                BufferedWriter bw = new BufferedWriter(fw);
                bw.write(s+"\r\n");//注意这里linux环境运行要改成"\r"来换行
                bw.close();
                fw.close();
            }
        } catch (Exception e) {
            //
        }
    }
    public static void ReadFileToCommandList(String filepath){
        try{
            File file = new File(filepath);
            FileInputStream fis = new FileInputStream(file);
            InputStreamReader is = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(is);
            String txtLine = null;
            while((txtLine=br.readLine())!=null){
                rawcommands.add(txtLine);
            }
            br.close();
        }catch(Exception e){
            e.printStackTrace();
        }
    }

    public static int getCommandTime(String command){
        int ind=command.indexOf(":");
        String timesring=command.substring(0,ind);
        return Integer.valueOf(timesring);
    }
    public static String getCommandType(String command){
        int indbegin=command.indexOf(":")+2;
        int indend=command.indexOf("(");
        String type=command.substring(indbegin,indend);
        return type;
    }
    public static ArrayList getCommandParameters(String command){
        ArrayList<Integer> list=new ArrayList<Integer>();
        int indbegin=command.indexOf("(")+1;
        int indend=command.indexOf(")");
        String raw=command.substring(indbegin,indend);
        String[] temp;
        if(raw.indexOf(",")==-1) {
            list.add(Integer.valueOf(raw));
            return list;
        }else{
            temp=raw.split(",");
            for(int i=0;i<temp.length;i++){
                list.add(Integer.valueOf(temp[i]));
            }
            return list;
        }
    }
    public Command stringToCommand(String rawcommand){
        int time=getCommandTime(rawcommand);
        String type=getCommandType(rawcommand);
        ArrayList<Integer> parameters=getCommandParameters(rawcommand);
        Command command=new Command(time,type,parameters);
        return command;
    }
    public static String tostringjobbyjob(Job job){
        String jobinfo;
        jobinfo="("+job.jobID+","+job.executed_time+","+job.total_time+")\n";
        return jobinfo;
    }
    public static boolean isfree(){
        return processor.runningjob==null;
    }
    public static void insertjob(Job job){
        heap.insert(job);
        rbt.insert(job);
    }
    public static void deletejobfromrbt(Job job){
        rbt.remove(job);
    }

    public Job searchbyid(int jobid){
        Job temp=new Job(jobid,0,0);
        if(rbt.mRoot==null){
            Job empty=new Job(0,0,0);
            return empty;
        }
        RBTree.RBTNode rst=rbt.search(rbt.mRoot,temp);
        if(rst!=null) {
            Job asw = rbt.search(rbt.mRoot, temp).getKey();
            if (asw == null) {
                Job empty = new Job(0, 0, 0);
                return empty;
            } else {
                return asw;
            }
        }else{
            Job empty = new Job(0, 0, 0);
            return empty;
        }
    }
    public Job searchnextbyid(int jobid){
        Job temp=new Job(jobid,0,0);
        Job asw=rbt.Next(rbt.mRoot,temp);
        if (asw==null){
            asw=new Job(0,0,0);
            return asw;
        }else {
            return asw;
        }
    }
    public Job searchprevious(int jobid){
        Job temp=new Job(jobid,0,0);
        Job asw=rbt.Prevoius(rbt.mRoot,temp);
        if (asw==null){
            asw=new Job(0,0,0);
            return asw;
        }else {
            return asw;
        }
    }
    public void between2idintolist(int jobid1,int jobid2){
        tempjoblist.clear();
        Job tempjob1=new Job(jobid1,0,0);
        Job tempjob2=new Job(jobid2,0,0);
        rbt.between(rbt.mRoot,tempjob1,tempjob2);
    }

    public class Command{
        public int arrivetime;
        public String command;
        public ArrayList<Integer> parameters;
        public Command(int time,String type,ArrayList para){
            this.arrivetime=time;
            this.command=type;
            this.parameters=para;
        }
    }

    public class Processor{
        public int roundtime;
        public Job runningjob;
        public Processor(int roundtime,Job job){
            this.runningjob=job;
            this.roundtime=roundtime;
        }
        public void init(){
            this.runningjob=null;
            this.roundtime=0;
        }
        public void process(){
            runningjob.executed_time++;
            roundtime++;
            if(runningjob.total_time-runningjob.executed_time==0){
                deletejobfromrbt(runningjob);
                roundtime=0;
                runningjob=null;
            }else if(roundtime==5){
                heap.insert(runningjob);
                roundtime=0;
                runningjob=null;
            }
        }
    }

    public class Scheduler{
        public void init(){
            ;
        }
        public void rawtoreal(){
            for(int i=0;i<rawcommands.size();i++){
                commands.add(stringToCommand(rawcommands.get(i)));
            }
        }
        public boolean ifthereiscommand(){
            return commands.size()!=0&&globletime==commands.get(0).arrivetime;
        }
        public void dealwithcommand(Command command){
            commands.remove(0);
            if(command.command.equals("Insert")){
                Job newjob=new Job((int)command.parameters.get(0),0,(int)command.parameters.get(1));
                insertjob(newjob);
            }else if(command.command.equals("NextJob")){
                writeToFile(tostringjobbyjob(searchnextbyid(command.parameters.get(0))));
            }else if(command.command.equals("PreviousJob")){
                writeToFile(tostringjobbyjob(searchprevious(command.parameters.get(0))));
            }else if(command.command.equals("PrintJob")){
                if(command.parameters.size()==1){
                    writeToFile(tostringjobbyjob(searchbyid(command.parameters.get(0))));
                }else{
                    between2idintolist(command.parameters.get(0),command.parameters.get(1));
                    String s=new String();
                    if(tempjoblist.size()!=0) {
                        for (int i = 0; i < tempjoblist.size(); i++) {
                            s += tostringjobbyjob(tempjoblist.get(i));
                            if (i != tempjoblist.size() - 1) {
                                s += ",";
                            }
                        }
                    }else{
                        Job nulljob=new Job(0,0,0);
                        s+=tostringjobbyjob(nulljob);
                    }
                    writeToFile(s);
                }
            }
        }

        public void dispatch(){
            Job nextjob;
            if(heap.size!=0) {
                nextjob = heap.removemin();
                processor.runningjob = nextjob;
            }
        }
        public void update(){
            if (ifthereiscommand()){
                dealwithcommand(commands.get(0));
            }
            if(isfree()){
                dispatch();
            }
            if(processor.runningjob==null&&commands.size()==0){
                System.exit(0);
            }
            if(processor.runningjob==null){
                ;
            }else{
                processor.process();
            }
            globletime++;
        }
    }

    public class Job implements Comparable<Job>{
        public int jobID;
        public int executed_time;
        public int total_time;
        public Job(int jobID,int executed_time,int total_time){
            this.jobID=jobID;
            this.executed_time=executed_time;
            this.total_time=total_time;
        }
        public int compareTo(Job job2){
            return this.jobID-job2.jobID;
        }
    }

    public class HeapMin {
        private Job[] Heap;
        private int maxsize;
        private int size;

        public HeapMin(int max) {
            maxsize = max;
            Heap = new Job[maxsize];
            size = 0;
            Heap[0] = null;
        }
        public void init(int max){
            maxsize = max;
            Heap = new Job[maxsize];
            size = 0;
            Heap[0] = null;
        }

        private int leftchild(int pos) {
            return 2 * pos;
        }
        private int rightchild(int pos) {
            return 2 * pos + 1;
        }

        private int parent(int pos) {
            return pos / 2;
        }
        private boolean haveparents(int pos){
            return pos/2!=0;
        }
        private boolean isleaf(int pos) {
            return ((pos > size / 2) && (pos <= size));
        }
        private void swap(int pos1, int pos2) {
            Job tmp;
            tmp = Heap[pos1];
            Heap[pos1] = Heap[pos2];
            Heap[pos2] = tmp;
        }
        public void insert(Job job) {
            size++;
            Heap[size] = job;
            int current = size;
            while (haveparents(current)&&Heap[current].executed_time < Heap[parent(current)].executed_time) {
                swap(current, parent(current));
                current = parent(current);
            }
        }

        public Job removemin() {
            swap(1, size);
            size--;
            if (size != 0)
                pushdown(1);
            return Heap[size + 1];
        }
        private void pushdown(int position) {
            int smallestchild;
            while (!isleaf(position)) {
                smallestchild = leftchild(position);
                if ((smallestchild < size)
                        && (Heap[smallestchild].executed_time > Heap[smallestchild + 1].executed_time))
                    smallestchild = smallestchild + 1;
                if (Heap[position].executed_time <= Heap[smallestchild].executed_time)
                    return;
                swap(position, smallestchild);
                position = smallestchild;
            }
        }
    }


    public class RBTree<T extends Comparable<T>> {
        private RBTNode<T> mRoot;
        private static final boolean RED   = false;
        private static final boolean BLACK = true;
        public class RBTNode<T extends Comparable<T>> {
            boolean color;
            T key;
            RBTNode<T> left;
            RBTNode<T> right;
            RBTNode<T> parent;
            public RBTNode(T key, boolean color, RBTNode<T> parent, RBTNode<T> left, RBTNode<T> right) {
                this.key = key;
                this.color = color;
                this.parent = parent;
                this.left = left;
                this.right = right;
            }
            public T getKey() {
                return key;
            }
            public String toString() {
                return ""+key+(this.color==RED?"(R)":"B");
            }
        }
        public RBTree() {
            mRoot=null;
        }
        private RBTNode<T> parentOf(RBTNode<T> node) {
            return node!=null ? node.parent : null;
        }
        private boolean colorOf(RBTNode<T> node) {
            return node!=null ? node.color : BLACK;
        }
        private boolean isRed(RBTNode<T> node) {
            return ((node!=null)&&(node.color==RED)) ? true : false;
        }
        private boolean isBlack(RBTNode<T> node) {
            return !isRed(node);
        }
        private void setBlack(RBTNode<T> node) {
            if (node!=null)
                node.color = BLACK;
        }
        private void setRed(RBTNode<T> node) {
            if (node!=null)
                node.color = RED;
        }
        private void setParent(RBTNode<T> node, RBTNode<T> parent) {
            if (node!=null)
                node.parent = parent;
        }
        private void setColor(RBTNode<T> node, boolean color) {
            if (node!=null)
                node.color = color;
        }

        public T Prevoius(RBTNode<T> node,T key) {
            if (node == null) {
                return null;
            } else if (node.key.compareTo(key) >= 0) {
                if (node.left == null) {
                    return null;
                } else {
                    return Prevoius(node.left, key);
                }
            } else if (node.key.compareTo(key) < 0) {
                if (node.right == null||node.right.key.compareTo(key)>=0) {
                    return node.key;
                } else {
                    return Prevoius(node.right, key);
                }
            }
            return null;
        }

        public T Next(RBTNode<T> node,T key) {
            if (node == null) {
                return null;
            } else if (node.key.compareTo(key) > 0) {
                if (node.left == null||node.left.key.compareTo(key)<=0) {
                    return node.key;
                } else {
                    return Next(node.left, key);
                }
            } else if (node.key.compareTo(key) <= 0) {
                if (node.right == null) {
                    return null;
                } else {
                    return Next(node.right, key);
                }
            }
            return null;
        }

        public void between(RBTNode<T> node,T key1,T key2){
            if(node==null){
                return;
            }else if(node.key.compareTo(key1)>0&&node.key.compareTo(key2)>=0){
                if(node.key.compareTo(key2)==0){
                    tempjoblist.add((Job)node.key);
                    between(node.left,key1,key2);
                }else{
                    between(node.left,key1,key2);
                }
            }else if(node.key.compareTo(key1)<=0&&node.key.compareTo(key2)<0){
                if(node.key.compareTo(key1)==0){
                    tempjoblist.add((Job)node.key);
                    between(node.right,key1,key2);
                }else{
                    between(node.right,key1,key2);
                }
            }else if(node.key.compareTo(key1)>0&&node.key.compareTo(key2)<0){
                between(node.left,key1,node.key);
                tempjoblist.add((Job) node.key);
                between(node.right,node.key,key2);
            }

        }


        public RBTNode<T> search(RBTNode<T> x, T key) {
            if (x==null){
                return x;
            }else {
                int cmp = key.compareTo(x.key);
                if (cmp < 0) {
                    if(x.left!=null) {
                        return search(x.left, key);
                    }else{
                        return null;
                    }
                }
                else if (cmp > 0) {
                    if(x.right!=null) {
                        return search(x.right, key);
                    }else{
                        return null;
                    }
                }
                else
                    return x;
            }
        }

        private RBTNode<T> minimum(RBTNode<T> tree) {
            if (tree == null)
                return null;
            while(tree.left != null)
                tree = tree.left;
            return tree;
        }
        public T minimum() {
            RBTNode<T> p = minimum(mRoot);
            if (p != null)
                return p.key;
            return null;
        }

        private RBTNode<T> maximum(RBTNode<T> tree) {
            if (tree == null)
                return null;
            while(tree.right != null)
                tree = tree.right;
            return tree;
        }
        public T maximum() {
            RBTNode<T> p = maximum(mRoot);
            if (p != null)
                return p.key;
            return null;
        }


        private void leftRotate(RBTNode<T> x) {
            RBTNode<T> y = x.right;
            x.right = y.left;
            if (y.left != null)
                y.left.parent = x;
            y.parent = x.parent;
            if (x.parent == null) {
                this.mRoot = y;
            } else {
                if (x.parent.left == x)
                    x.parent.left = y;
                else
                    x.parent.right = y;
            }

            y.left = x;
            x.parent = y;
        }

        private void rightRotate(RBTNode<T> y) {
            RBTNode<T> x = y.left;
            y.left = x.right;
            if (x.right != null)
                x.right.parent = y;
            x.parent = y.parent;
            if (y.parent == null) {
                this.mRoot = x;
            } else {
                if (y == y.parent.right)
                    y.parent.right = x;
                else
                    y.parent.left = x;
            }
            x.right = y;
            y.parent = x;
        }

        private void insertFixUp(RBTNode<T> node) {
            RBTNode<T> parent, gparent;
            while (((parent = parentOf(node))!=null) && isRed(parent)) {
                gparent = parentOf(parent);
                if (parent == gparent.left) {
                    RBTNode<T> uncle = gparent.right;
                    if ((uncle!=null) && isRed(uncle)) {
                        setBlack(uncle);
                        setBlack(parent);
                        setRed(gparent);
                        node = gparent;
                        continue;
                    }
                    if (parent.right == node) {
                        RBTNode<T> tmp;
                        leftRotate(parent);
                        tmp = parent;
                        parent = node;
                        node = tmp;
                    }
                    setBlack(parent);
                    setRed(gparent);
                    rightRotate(gparent);
                } else {
                    RBTNode<T> uncle = gparent.left;
                    if ((uncle!=null) && isRed(uncle)) {
                        setBlack(uncle);
                        setBlack(parent);
                        setRed(gparent);
                        node = gparent;
                        continue;
                    }
                    if (parent.left == node) {
                        RBTNode<T> tmp;
                        rightRotate(parent);
                        tmp = parent;
                        parent = node;
                        node = tmp;
                    }
                    setBlack(parent);
                    setRed(gparent);
                    leftRotate(gparent);
                }
            }
            setBlack(this.mRoot);
        }

        private void insert(RBTNode<T> node) {
            int cmp;
            RBTNode<T> y = null;
            RBTNode<T> x = this.mRoot;
            while (x != null) {
                y = x;
                cmp = node.key.compareTo(x.key);
                if (cmp < 0)
                    x = x.left;
                else
                    x = x.right;
            }
            node.parent = y;
            if (y!=null) {
                cmp = node.key.compareTo(y.key);
                if (cmp < 0)
                    y.left = node;
                else
                    y.right = node;
            } else {
                this.mRoot = node;
            }
            node.color = RED;
            insertFixUp(node);
        }

        public void insert(T key) {
            RBTNode<T> node=new RBTNode<T>(key,BLACK,null,null,null);
            if (node != null)
                insert(node);
        }
        private void removeFixUp(RBTNode<T> node, RBTNode<T> parent) {
            RBTNode<T> other;
            while ((node==null || isBlack(node)) && (node != this.mRoot)) {
                if (parent.left == node) {
                    other = parent.right;
                    if (isRed(other)) {
                        setBlack(other);
                        setRed(parent);
                        leftRotate(parent);
                        other = parent.right;
                    }
                    if ((other.left==null || isBlack(other.left)) &&
                            (other.right==null || isBlack(other.right))) {
                        setRed(other);
                        node = parent;
                        parent = parentOf(node);
                    } else {
                        if (other.right==null || isBlack(other.right)) {
                            setBlack(other.left);
                            setRed(other);
                            rightRotate(other);
                            other = parent.right;
                        }
                        setColor(other, colorOf(parent));
                        setBlack(parent);
                        setBlack(other.right);
                        leftRotate(parent);
                        node = this.mRoot;
                        break;
                    }
                } else {
                    other = parent.left;
                    if (isRed(other)) {
                        setBlack(other);
                        setRed(parent);
                        rightRotate(parent);
                        other = parent.left;
                    }
                    if ((other.left==null || isBlack(other.left)) &&
                            (other.right==null || isBlack(other.right))) {
                        setRed(other);
                        node = parent;
                        parent = parentOf(node);
                    } else {
                        if (other.left==null || isBlack(other.left)) {
                            setBlack(other.right);
                            setRed(other);
                            leftRotate(other);
                            other = parent.left;
                        }
                        setColor(other, colorOf(parent));
                        setBlack(parent);
                        setBlack(other.left);
                        rightRotate(parent);
                        node = this.mRoot;
                        break;
                    }
                }
            }
            if (node!=null)
                setBlack(node);
        }

        private void remove(RBTNode<T> node) {
            RBTNode<T> child, parent;
            boolean color;
            if ( (node.left!=null) && (node.right!=null) ) {
                RBTNode<T> replace = node;
                replace = replace.right;
                while (replace.left != null)
                    replace = replace.left;
                if (parentOf(node)!=null) {
                    if (parentOf(node).left == node)
                        parentOf(node).left = replace;
                    else
                        parentOf(node).right = replace;
                } else {
                    this.mRoot = replace;
                }
                child = replace.right;
                parent = parentOf(replace);
                color = colorOf(replace);
                if (parent == node) {
                    parent = replace;
                } else {
                    if (child!=null)
                        setParent(child, parent);
                    parent.left = child;
                    replace.right = node.right;
                    setParent(node.right, replace);
                }
                replace.parent = node.parent;
                replace.color = node.color;
                replace.left = node.left;
                node.left.parent = replace;
                if (color == BLACK)
                    removeFixUp(child, parent);
                node = null;
                return ;
            }
            if (node.left !=null) {
                child = node.left;
            } else {
                child = node.right;
            }
            parent = node.parent;
            color = node.color;
            if (child!=null)
                child.parent = parent;
            if (parent!=null) {
                if (parent.left == node)
                    parent.left = child;
                else
                    parent.right = child;
            } else {
                this.mRoot = child;
            }
            if (color == BLACK)
                removeFixUp(child, parent);
            node = null;
        }

        public void remove(T key) {
            RBTNode<T> node;
            if ((node = search(mRoot, key)) != null)
                remove(node);
        }

        private void destroy(RBTNode<T> tree) {
            if (tree==null)
                return ;
            if (tree.left != null)
                destroy(tree.left);
            if (tree.right != null)
                destroy(tree.right);
            tree=null;
        }

        public void clear() {
            destroy(mRoot);
            mRoot = null;
        }
    }

    public static void main(String[] args) {
        Main m=new Main();
        try{
            creatTxtFile(outputpath);
        }catch (Exception e){
            ;
        }
        scheduler=m.newscheduler();
        heap=m.newheap();
        rbt=m.newrbt();
        processor=m.newprocessor();
        scheduler.init();
        ReadFileToCommandList(args[0]);
        scheduler.rawtoreal();
        while (true){
            scheduler.update();
        }
    }
}
